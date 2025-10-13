import math, random, time
from .heuristic import h_partial
   
def simulated_annealing(n, goal, heuristic=h_partial, max_iter=10000):
    start_time = time.time()
    goal = list(goal) if isinstance(goal, tuple) else goal

    current = []  # bắt đầu rỗng

    steps_visual = []
    steps_console = []

    expanded_count = 0
    visited_count = 0

    t = 1
    for _ in range(max_iter):
        T = max(0.01, 1000 / (t + 1))
        visited_count += 1

        curr_h = heuristic(current, goal)
        steps_visual.append(current[:])
        steps_console.append((t, round(T, 3), current[:], curr_h))

        if current == goal:
            elapsed = (time.time() - start_time) * 1000
            stats = {
                "expanded": expanded_count,
                "visited": visited_count,
                "frontier": 0,
                "time": elapsed
            }
            return current, steps_visual, stats

        successors = []
        row = len(current)
        if row < n:
            for col in range(n):
                if col not in current:
                    successors.append(current + [col])

        expanded_count += len(successors)
        if not successors:
            break

        scored = [(heuristic(s, goal), s) for s in successors]
        scored.sort(key=lambda x: x[0])
        best_s_h, best_s = scored[0]

        if best_s_h < curr_h:
            current = best_s
        else:
            next_state = random.choice(successors)
            deltaE = curr_h - heuristic(next_state, goal)
            if deltaE > 0:
                current = next_state
            else:
                if random.random() < math.exp(deltaE / T):
                    current = next_state

        t += 1

    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": 0,
        "time": elapsed
    }

    return None, steps_visual, stats

def simulated_annealing_visual(n, goal, return_steps=False, return_stats=False, return_logs=False, heuristic=h_partial, max_iter=10000):
    start_time = time.time()
    goal = list(goal) if isinstance(goal, tuple) else goal

    current = []
    steps_visual = []
    expanded_count = 0
    visited_count = 0
    logs = []

    t = 1
    for _ in range(max_iter):
        T = max(0.01, 1000 / (t + 1))
        visited_count += 1

        curr_h = heuristic(current, goal)
        steps_visual.append(current[:])
        s = ""
        s += f"{t}| T = {round(T,3)}, Current: {current} (h={curr_h})"

        if current == goal:
            elapsed = (time.time() - start_time) * 1000
            stats = {
                "expanded": expanded_count,
                "visited": visited_count,
                "frontier": 0,
                "time": elapsed
            }
            logs.append(s)
            if return_stats and return_logs:
                    return current, steps_visual, stats, logs
            elif return_logs:
                return current, steps_visual, logs
            elif return_stats:
                return current, steps_visual, stats
            return (current, steps_visual) if return_steps else current

        successors = []
        row = len(current)
        if row < n:
            for col in range(n):
                if col not in current:
                    next_state = current + [col]
                    successors.append((heuristic(next_state, goal), next_state))
                    expanded_count += 1

        succs = [f"{h}:{s}" for h, s in successors]
        s += f" | Successors: {succs}"

        if not successors:
            logs.append("No solution found.")
            break

        best_s_h, best_s = min(successors, key=lambda x: x[0])

        if best_s_h < curr_h:
            logs.append(s)
            current = best_s
        else:
            next_h, next_state = random.choice(successors)
            deltaE = curr_h - next_h
            if deltaE > 0:
                current = next_state
            else:
                r = random.random()
                acp = math.exp(deltaE / T)
                s += f" | Random: {next_state} ({acp}), {r}"
                logs.append(s)
                if r < acp:
                    current = next_state

        t += 1

    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": 0,
        "time": elapsed
    }

    logs.append("No solution found.")

    if return_stats and return_logs:
        return None, steps_visual, stats, logs
    elif return_logs:
        return None, steps_visual, logs
    elif return_stats:
        return None, steps_visual, stats
    return (None, steps_visual) if return_steps else None
