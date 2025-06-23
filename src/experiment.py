import argparse
import csv
import glob
import math
import multiprocessing as mp
import time

from sim.environment import Environment
from algo.risk_aware_alg import RiskAwareDStar
from algo.a_star import AStar


def run_trial(args):
    """
    Run one trial on a single map with given parameters.
    Returns a dict of results.
    """
    map_path, lam, r = args
    # Setup environment
    env = Environment(size=64, max_steps=128)
    env.load_map(map_path)

    # Initialize planners
    ev = RiskAwareDStar(size=64,
                        start=env.evader_start,
                        goal=env.evader_goal,
                        env=env,
                        r=r,
                        lambda_=lam)
    ch = AStar(size=64, env=env)

    # Reset initial positions
    env.evader_pos = env.evader_start
    env.pursuer_pos = (63, 0)
    env.step_count = 0
    env.done = env.caught = env.reached_goal = False

    total_cost = 0.0
    total_plan_time = 0.0
    steps = 0

    while not env.done and steps < env.max_steps:
        # Evader planning
        t0 = time.perf_counter()
        path = ev.plan(new_start=env.evader_pos, pursuer_pos=env.pursuer_pos)
        t1 = time.perf_counter()
        total_plan_time += (t1 - t0)
        move = path[0] if path else (0, 0)

        # Accumulate cost
        new_pos = (env.evader_pos[0] + move[0], env.evader_pos[1] + move[1])
        total_cost += env.get_cost(new_pos)

        # Pursuer planning with interception
        chase = ch.plan(env.pursuer_pos, env.evader_pos, env.evader_goal, r)
        pu_move = chase[0] if chase else (0, 0)

        # Step environment
        env.step(evader_move=move, pursuer_move=pu_move)
        steps += 1

    return {
        'map': map_path,
        'lambda': lam,
        'r': r,
        'steps': steps,
        'caught': int(env.caught),
        'reached': int(env.reached_goal),
        'path_cost': total_cost,
        'avg_plan_time': (total_plan_time / steps) if steps else None
    }


def main():
    parser = argparse.ArgumentParser(description="Batch experiments for Risk-Aware D* Lite.")
    parser.add_argument('--maps-dir', default='../map/', help='Directory containing CSV map files')
    parser.add_argument('--output', default='../data/experiment_results.csv', help='CSV output file')
    parser.add_argument('--workers', type=int, default=mp.cpu_count(), help='Number of parallel processes')
    args = parser.parse_args()

    # Gather tasks
    map_files = sorted(glob.glob(f"{args.maps_dir}/*.csv"))
    lam_values = [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
    r_values = list(range(0, 11))
    tasks = [(m, lam, r) for m in map_files for lam in lam_values for r in r_values]

    # Parallel execution
    with mp.Pool(processes=args.workers) as pool:
        results = pool.map(run_trial, tasks)

    # Write out CSV
    with open(args.output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"Wrote {len(results)} rows to {args.output}")

if __name__ == '__main__':
    main()
