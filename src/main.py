import argparse
import ctypes
import sys

from sim.environment import Environment
from algo.a_star import AStar
from algo.d_star_lite import DStarLite
from gui.display import Display

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
    return parser.parse_args()


def main():
    args = parse_args()

    # Initialize environment
    env = Environment(size=args.grid_size, max_steps=args.max_steps, seed=args.seed)

    # Initialize planners
    evader = DStarLite(size=args.grid_size, start=env.evader_pos, goal=env.evader_goal)
    pursuer = AStar(size=args.grid_size)

    # Initialize display (controls discrete time interval via fps)
    display = Display(env, cell_size=args.cell_size, fps=args.fps)

    # Initial render to ensure window shows before planning
    display.render()

    # Main simulation loop
    while not env.done:
        # Debug: print positions
        print(f"Step {env.step_count}: Evader at {env.evader_pos}, Pursuer at {env.pursuer_pos}")

        # Evader plans path
        ev_path = evader.plan(new_start=env.evader_pos)
        ev_move = ev_path[0] if ev_path else (0, 0)

        # Pursuer plans chase
        chase_path = pursuer.plan(env.pursuer_pos, env.evader_pos)
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
    display.quit()


if __name__ == "__main__":
    main()
