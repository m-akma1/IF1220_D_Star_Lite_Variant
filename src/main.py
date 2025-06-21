import argparse
import ctypes
import sys

from sim.environment import Environment
from sim.display import Display
from algo.a_star import AStar
from algo.d_star_lite import DStarLite
from algo.risk_aware_alg import RiskAwareDStar

# Optional DPI awareness for Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


def parse_args():
    parser = argparse.ArgumentParser(
        description="Pursuit-Evasion Simulation: Evader (D* Lite) vs. Pursuer (A*)"
    )
    parser.add_argument(
        "--grid-size", type=int, default=64,
        help="Dimension N for an NxN grid"
    )
    parser.add_argument(
        "--max-steps", type=int, default=500,
        help="Maximum number of discrete time steps before timeout"
    )
    parser.add_argument(
        "--fps", type=int, default=5,
        help="Simulation frames per second (inverse of time interval)"
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--cell-size", type=int, default=10,
        help="Pixel size per grid cell in the GUI"
    )
    parser.add_argument(
      '--load-map', 
      help='Path to CSV map file to initialize terrain'
    )
    parser.add_argument(
      '--save-map', 
      help='Path to CSV file to dump final terrain'
    )
    parser.add_argument(
      '--radius', 
      help='Radius in which the evader flee from pursuer'
    )
    parser.add_argument(
      '--penalty', 
      help='Penalty constant for the risk function'
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Initialize environment
    env = Environment(size=args.grid_size, max_steps=args.max_steps, seed=args.seed)

    RISK_RADIUS = int(args.radius) if args.radius else 1
    PENALTY_FACTOR = float(args.penalty) if args.penalty else 0

    # Initialize planners
    evader = RiskAwareDStar(size=args.grid_size, start=env.evader_pos, goal=env.evader_goal, env=env, r=RISK_RADIUS, lambda_=PENALTY_FACTOR)
    pursuer = AStar(size=args.grid_size, env=env)

    if args.load_map:
        env.load_map(args.load_map)
        evader._initialize()

    # Initialize display (controls discrete time interval via fps)
    display = Display(env, cell_size=args.cell_size, fps=args.fps, evader_planner=evader)

    # Initial render to ensure window shows before planning
    display.render()

    # Main simulation loop
    while not env.done:
        # Debug: print positions
        print(f"Step {env.step_count}: Evader at {env.evader_pos}, Pursuer at {env.pursuer_pos}")

        # Evader plans path
        ev_path = evader.plan(new_start=env.evader_pos, pursuer_pos=env.pursuer_pos)
        ev_move = ev_path[0] if ev_path else (0, 0)

        # Pursuer plans chase
        chase_path = pursuer.plan(env.pursuer_pos, env.evader_pos, env.evader_goal, RISK_RADIUS)
        pu_move = chase_path[0] if chase_path else (0, 0)

        # Advance environment by one discrete time step
        env.step(evader_move=ev_move, pursuer_move=pu_move)

        # Render current state and enforce time interval
        display.render()

    # Simulation ended: report summary
    summary = (
        f"Steps: {env.step_count} | "
        f"Caught: {env.caught} | "
        f"Reached Goal: {env.reached_goal}"
    )
    print(summary)
    
    if args.save_map:
        env.save_map(args.save_map)
    display.quit()


if __name__ == "__main__":
    main()
