import time
from .heuristic import h_partial

def hill_climbing(n, goal, heuristic=h_partial):
    start_time = time.time()
    goal = list(goal) if isinstance(goal, tuple) else goal

    current = []
    steps_visual = []
    expanded_count = 0
    visited_count = 0

    while True:
        steps_visual.append(current[:])
        visited_count += 1
        row = len(current)
        if row == n:
            elapsed = (time.time() - start_time) * 1000
            stats = {
                "expanded": expanded_count,
                "visited": visited_count,
                "frontier": 0,
                "time": elapsed
            }
            return (current if current == goal else None), steps_visual, stats

        # Sinh tất cả con hợp lệ
        candidates = []
        for col in range(n):
            if col not in current:
                next_state = current + [col]
                candidates.append((heuristic(next_state, goal), next_state))
                expanded_count += 1

        if not candidates:
            break

        best_h, best_state = min(candidates, key=lambda x: x[0])
        curr_h = heuristic(current, goal)

        # Nếu không cải thiện -> dừng
        if best_h >= curr_h:
            break

        # Di chuyển đến child tốt nhất
        current = best_state

    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": 0,
        "time": elapsed
    }
    return None, steps_visual, stats


def hill_climbing_visual(n, goal, return_steps=False, return_stats=False, return_logs=False, heuristic=h_partial):
    start_time = time.time()
    goal = list(goal) if isinstance(goal, tuple) else goal

    current = []
    steps_visual = []
    expanded_count = 0
    visited_count = 0
    logs = []

    while True:
        steps_visual.append(current[:])
        visited_count += 1
        curr_h = heuristic(current, goal)
        s = ""
        s += f"Current: {current} (heuristic={curr_h})"
        
        row = len(current)
        if row == n:
            elapsed = (time.time() - start_time) * 1000
            stats = {
                "expanded": expanded_count,
                "visited": visited_count,
                "frontier": 0,
                "time": elapsed
            }
            logs.append(s)
            # return (current if current == goal else None), steps_visual, stats
            if return_stats and return_logs:
                    return current, steps_visual, stats, logs
            elif return_logs:
                return current, steps_visual, logs
            elif return_stats:
                return current, steps_visual, stats
            return (current, steps_visual) if return_steps else current    

        candidates = []
        for col in range(n):
            if col not in current:
                next_state = current + [col]
                candidates.append((heuristic(next_state, goal), next_state))
                expanded_count += 1

        neighbor = [f"{h}:{s}" for h, s in candidates]
        s += f" | Neighbors: {neighbor}"
        logs.append(s)

        if not candidates:
            logs.append("No solution found.")
            break

        best_h, best_state = min(candidates, key=lambda x: x[0])

        if best_h >= curr_h:
            logs.append("No solution found.")
            break

        current = best_state

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