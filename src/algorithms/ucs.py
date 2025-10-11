import heapq
import itertools
import time
from .cost import placement_cost_goal

def uniform_cost_search(n, goal, placement_cost_goal=placement_cost_goal):
    """
    Uniform Cost Search (UCS)
    - visited: số trạng thái đã được lấy ra khỏi hàng đợi để xét
    - expanded: tổng số trạng thái con đã được sinh ra
    - frontier: số trạng thái còn lại trong hàng đợi (heap)
    """
    if isinstance(goal, tuple):
        goal = list(goal)

    start_time = time.time()
    counter = itertools.count()  # Bộ đếm tăng dần

    heap = [(0, next(counter), [])]  # (cost, count, state)
    visited = set()
    steps_visual = []
    expanded_count = 0
    visited_count = 0

    while heap:
        cost, _, state = heapq.heappop(heap)
        steps_visual.append(state)
        visited_count += 1

        row = len(state)
        if row == n:
            if state == goal:
                elapsed = (time.time() - start_time) * 1000
                stats = {
                    "expanded": expanded_count,
                    "visited": visited_count,
                    "frontier": len(heap),
                    "time": elapsed
                }
                return state, steps_visual, stats
            continue

        if tuple(state) in visited:
            continue
        visited.add(tuple(state))

        for col in range(n):
            if col not in state:
                step_cost = placement_cost_goal(state, row, col, goal)
                new_cost = cost + step_cost
                new_state = state + [col]
                heapq.heappush(heap, (new_cost, next(counter), new_state))
                expanded_count += 1

    # Không tìm thấy lời giải
    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": len(heap),
        "time": elapsed
    }
    return None, steps_visual, stats

def uniform_cost_search_visual(n, goal, return_steps=False, return_stats=False, return_logs=False, placement_cost_goal=placement_cost_goal):
    """
    Uniform Cost Search (UCS) có Visualization.
    - Ghi lại toàn bộ log và bước mở rộng.
    - Cho phép hiển thị trong panel visualize từng bước.
    """
    if isinstance(goal, tuple):
        goal = list(goal)

    start_time = time.time()
    counter = itertools.count()

    heap = [(0, next(counter), [])]
    visited = set()
    steps = []         # các state được lấy ra khỏi heap
    logs = []          # log chi tiết
    expanded_count = 0
    visited_count = 0

    while heap:
        cost, _, state = heapq.heappop(heap)
        steps.append(state)
        visited_count += 1
        s = ""
        # Log trạng thái hiện tại
        heap_snapshot = [f"{c}:{s}" for c, _, s in heap]
        s += f"Pop: {state} (cost={cost}) | Frontier: {heap_snapshot}"
        print(f"Pop: {state} (cost={cost}) | Frontier: {heap_snapshot}")

        row = len(state)
        if row == n:
            if state == goal:
                elapsed = (time.time() - start_time) * 1000
                stats = {
                    "expanded": expanded_count,
                    "visited": visited_count,
                    "frontier": len(heap),
                    "time": elapsed
                }
                logs.append(s)
                print(f"FOUND GOAL: {state} (total cost={cost:.2f})")
                if return_stats and return_logs:
                    return state, steps, stats, logs
                elif return_logs:
                    return state, steps, logs
                elif return_stats:
                    return state, steps, stats
                return (state, steps) if return_steps else state
            continue

        # Bỏ qua nếu đã thăm
        if tuple(state) in visited:
            print(f"Skip visited: {state}")
            continue
        visited.add(tuple(state))

        # Mở rộng node hiện tại
        for col in range(n):
            if col not in state:
                step_cost = placement_cost_goal(state, row, col, goal)
                new_cost = cost + step_cost
                new_state = state + [col]
                heapq.heappush(heap, (new_cost, next(counter), new_state))
                expanded_count += 1
                print(f"→ Push: {new_state} (cost={new_cost:.2f})")
        
        heap_snapshot = [f"{c}:{s}" for c, _, s in heap]
        s += f" | Updated Frontier: {heap_snapshot}"
        logs.append(s)

    # Nếu không tìm thấy lời giải
    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": len(heap),
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