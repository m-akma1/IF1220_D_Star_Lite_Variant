from sim.environment import Environment
from algo.risk_aware_alg import RiskAwareDStar
from algo.a_star import AStar
import time, csv, glob

map_files = sorted(glob.glob("../setup/*.csv"))

results = []
for map_path in map_files:
    # load the map
    env = Environment(size=64, max_steps=128)
    env.load_map(map_path)

    for lam in (1,2,3):
      for r in range(2,13):
        # re-initialize planners
        ev = RiskAwareDStar(
            size=64, start=env.evader_start, goal=env.evader_goal,
            env=env, r=r, lambda_=lam)
        ch = AStar(size=64, env=env)

        # run one trial
        env.evader_pos = env.evader_start
        env.pursuer_pos = (0,63)
        env.step_count = 0
        env.done = env.caught = env.reached_goal = False

        total_cost = 0
        total_plan_time = 0
        steps = 0

        while not env.done and steps <= 128:
            t0 = time.perf_counter()
            path = ev.plan(new_start=env.evader_pos,
                           pursuer_pos=env.pursuer_pos)
            plan_time = time.perf_counter() - t0
            move = path[0] if path else (0,0)
            total_plan_time += plan_time

            # accumulate cost of that step
            total_cost += env.get_cost((env.evader_pos[0]+move[0], env.evader_pos[1]+move[1]))

            # pursuer intercept
            chase = ch.plan_intercept(env.pursuer_pos,
                                      env.evader_pos,
                                      env.evader_goal)
            pu_move = chase[0] if chase else (0,0)

            env.step(evader_move=move, pursuer_move=pu_move)
            steps += 1
            print(steps)

        results.append({
          "map": map_path,
          "lambda": lam,
          "r": r,
          "steps": steps,
          "caught": int(env.caught),
          "reached": int(env.reached_goal),
          "path_cost": total_cost,
          "avg_plan_time": total_plan_time / steps if steps else None
        })

with open("experiment_results.csv","w",newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
