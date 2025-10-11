import heapq
import itertools
import time
from .heuristic import h_misplaced

def greedy_best_search(n=8, goal=None, heuristic=h_misplaced):
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    start_time = time.time()
    open_list = []
    steps_visual = []
    visited = set()

    counter = itertools.count()
    expanded_count = 0
    visited_count = 0

    # trạng thái ban đầu
    h0 = heuristic([], goal) if heuristic and goal else (n - 0)
    heapq.heappush(open_list, (h0, next(counter), []))

    while open_list:
        h, _, state = heapq.heappop(open_list)
        steps_visual.append(state)
        visited_count += 1

        # kiểm tra goal
        if len(state) == n:
            if goal is None or state == goal:
                elapsed = (time.time() - start_time) * 1000
                stats = {
                    "expanded": expanded_count,
                    "visited": visited_count,
                    "frontier": len(open_list),
                    "time": elapsed
                }
                return state, steps_visual, stats
            continue

        if tuple(state) in visited:
            continue
        visited.add(tuple(state))

        # mở rộng node hiện tại
        for col in range(n):
            if col not in state:
                new_state = state + [col]
                new_h = heuristic(new_state, goal) if heuristic and goal else (n - len(new_state))
                heapq.heappush(open_list, (new_h, next(counter), new_state))
                expanded_count += 1

    # không tìm thấy lời giải
    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": len(open_list),
        "time": elapsed
    }
    return None, steps_visual, stats

def greedy_best_search_visual(
    n=8, goal=None, return_steps=False, return_stats=False,
    return_logs=False, heuristic=h_misplaced
):
    """
    Greedy Best-First Search (visual version)
    - Log chi tiết Pop / Push / Frontier mỗi vòng.
    """
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    start_time = time.time()
    open_list = []
    visited = set()

    steps = []  # lưu state pop ra (để visualize)
    logs = []   # log chi tiết từng bước
    expanded_count = 0
    visited_count = 0
    counter = itertools.count()

    h0 = heuristic([], goal) if heuristic and goal else (n - 0)
    heapq.heappush(open_list, (h0, next(counter), []))

    while open_list:
        h, _, state = heapq.heappop(open_list)
        steps.append(state)
        visited_count += 1
        s = ""
        queue_view = [f"{h}:{s}" for h, _, s in open_list]
        s += f"Pop: {state} | h={h:.1f} | Frontier: {queue_view}"
        print(f"Pop: {state} | h={h:.1f} | Frontier: {queue_view}")

        if len(state) == n:
            if goal is None or state == goal:
                elapsed = (time.time() - start_time) * 1000
                stats = {
                    "expanded": expanded_count,
                    "visited": visited_count,
                    "frontier": len(open_list),
                    "time": elapsed
                }
                logs.append(s)
                print(f"GOAL FOUND: {state} | Total time={elapsed:.1f}ms")
                if return_stats and return_logs:
                    return state, steps, stats, logs
                elif return_logs:
                    return state, steps, logs
                elif return_stats:
                    return state, steps, stats
                return (state, steps) if return_steps else state
            continue

        if tuple(state) in visited:
            print(f"Skip visited: {state}")
            continue
        visited.add(tuple(state))

        for col in range(n):
            if col not in state:
                new_state = state + [col]
                new_h = heuristic(new_state, goal) if heuristic and goal else (n - len(new_state))
                heapq.heappush(open_list, (new_h, next(counter), new_state))
                expanded_count += 1
                print(f"→ Push: {new_state} | h={new_h:.1f}")

        queue_view = [f"{h}:{s}" for f, _, s in open_list]
        s += f" | Updated Frontier: {queue_view}"
        logs.append(s)

    # --- Không tìm thấy ---
    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": len(open_list),
        "time": elapsed
    }
    logs.append("No solution found.")

    if return_stats and return_logs:
        return None, steps, stats, logs
    elif return_logs:
        return None, steps, logs
    elif return_stats:
        return None, steps, stats
    return (None, steps) if return_steps else None