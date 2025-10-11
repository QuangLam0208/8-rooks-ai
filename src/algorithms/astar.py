import heapq
import itertools
import time
from .cost import placement_cost_goal
from .heuristic import h_misplaced

def a_star_search(n=8, goal=None,
                  placement_cost=placement_cost_goal, heuristic=h_misplaced):
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    counter = itertools.count()
    open_list = []
    heapq.heappush(open_list, (0, next(counter), 0, 0, []))  # f=0, count, g=0, h=0, state rỗng
    visited = set()
    steps_visual = []   # từng node pop ra

    expanded_count = 0
    visited_count = 0
    start_time = time.time()

    while open_list:
        f, _, g, h, state = heapq.heappop(open_list)
        steps_visual.append(state[:])
        visited_count += 1

        row = len(state)
        # Kiểm tra goal
        if row == n:
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

        # Mở rộng node hiện tại
        for col in range(n):
            if col not in state:  # không trùng cột
                # g(n+1): chi phí thực tế
                step_cost = placement_cost(state, row, col, goal) if placement_cost else 1
                new_g = g + step_cost
                new_state = state + [col]

                # h(n+1): heuristic
                new_h = heuristic(new_state, goal) if heuristic and goal else (n - len(new_state))

                # f = g + h
                new_f = new_g + new_h
                heapq.heappush(open_list, (new_f, next(counter), new_g, new_h, new_state))
                expanded_count += 1

    # Không tìm thấy goal
    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": len(open_list),
        "time": elapsed
    }
    return None, steps_visual, stats

def a_star_search_visual(n=8, goal=None, return_steps=False, return_stats=False,
                         return_logs=False,
                         placement_cost=placement_cost_goal, heuristic=h_misplaced):
    """
    A* Search có Visualization cho bài toán n quân xe.
    - Ghi log chi tiết từng bước (f = g + h).
    - Dùng cho animation & hiển thị log trong giao diện.
    """
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    counter = itertools.count()
    open_list = []
    heapq.heappush(open_list, (0, next(counter), 0, 0, []))  # (f=0, count, g=0, h=0, state rỗng)
    visited = set()

    steps = []  # Các state được pop ra để visualize
    logs = []   # Các dòng log chi tiết
    expanded_count = 0
    visited_count = 0

    start_time = time.time()

    while open_list:
        f,_, g, h, state = heapq.heappop(open_list)
        steps.append(state[:])
        visited_count += 1
        s = ""
        
        queue_view = [f"{f}:{s}" for f, _, _, _, s in open_list]
        s += f"Pop: {state} | f={f:.1f}, g={g:.1f}, h={h:.1f} | Frontier: {queue_view}"
        print(f"Pop: {state} | f={f:.1f}, g={g:.1f}, h={h:.1f} | Frontier: {queue_view}")

        row = len(state)
        if row == n:
            if goal is None or state == goal:
                elapsed = (time.time() - start_time) * 1000
                stats = {
                    "expanded": expanded_count,
                    "visited": visited_count,
                    "frontier": len(open_list),
                    "time": elapsed
                }
                logs.append(s)
                print(f"GOAL FOUND: {state} | f={f:.1f}, total time={elapsed:.1f}ms")
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

        # Mở rộng các node con
        for col in range(n):
            if col not in state:
                step_cost = placement_cost(state, row, col, goal) if placement_cost else 1
                new_g = g + step_cost
                new_state = state + [col]

                new_h = heuristic(new_state, goal) if heuristic and goal else (n - len(new_state))
                new_f = new_g + new_h

                heapq.heappush(open_list, (new_f, next(counter), new_g, new_h, new_state))
                expanded_count += 1
                print(f"→ Push: {new_state} | g={new_g:.1f}, h={new_h:.1f}, f={new_f:.1f}")

        queue_view = [f"{f}:{s}" for f, _, _, _, s in open_list]
        s += f" | Updated Frontier: {queue_view}"
        logs.append(s)

    # Không tìm thấy lời giải
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