from collections import deque
import time

def breadth_first_search(n, goal=None, return_steps=False, return_stats=False):
    """
    BFS đặt n quân xe.
    - visited: số trạng thái đã được xét (lấy ra khỏi queue)
    - expanded: tổng số trạng thái con đã sinh ra
    - frontier: số trạng thái còn lại trong queue
    """
    start_time = time.time()
    queue = deque([[]])  
    visited_count = 0     # số node đã được xét
    expanded_count = 0    # số node được sinh ra
    steps = []  

    while queue:
        state = queue.popleft()
        visited_count += 1
        steps.append(state)

        row = len(state)
        if row == n:
            if goal is not None and isinstance(goal, tuple):
                goal = list(goal)
            if state == goal:
                elapsed = (time.time() - start_time) * 1000
                stats = {
                    "expanded": expanded_count,
                    "visited": visited_count,
                    "frontier": len(queue),
                    "time": elapsed
                }
                if return_stats:
                    return (state, steps, stats)
                return (state, steps) if return_steps else state
            continue

        # mở rộng node hiện tại
        for col in range(n):
            if col not in state:
                new_state = state + [col]
                queue.append(new_state)
                expanded_count += 1  # tăng số node sinh ra

    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": len(queue),
        "time": elapsed
    }

    if return_stats:
        return (None, steps, stats)
    return (None, steps) if return_steps else None

def breadth_first_search_visual(n, goal=None, return_steps=False, return_stats=False, return_logs=False):
    """
    BFS đặt n quân xe, thêm log chi tiết để visualize từng bước.
    """
    start_time = time.time()
    queue = deque([[]])
    visited_count = 0
    expanded_count = 0
    steps = []
    logs = []

    while queue:
        state = queue.popleft()
        visited_count += 1
        steps.append(state)

        # Ghi log state hiện tại + queue hiện tại
        queue_snapshot = list(queue)
        logs.append(f"State {visited_count - 1}: {state} | Queue: {queue_snapshot}")

        row = len(state)
        if row == n:
            if goal is not None and isinstance(goal, tuple):
                goal = list(goal)
            if state == goal:
                elapsed = (time.time() - start_time) * 1000
                stats = {
                    "expanded": expanded_count,
                    "visited": visited_count,
                    "frontier": len(queue),
                    "time": elapsed
                }
                if return_stats and return_logs:
                    return (state, steps, stats, logs)
                elif return_logs:
                    return (state, steps, logs)
                elif return_stats:
                    return (state, steps, stats)
                return (state, steps) if return_steps else state
            continue

        # mở rộng node hiện tại
        for col in range(n):
            if col not in state:
                new_state = state + [col]
                queue.append(new_state)
                expanded_count += 1

    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": len(queue),
        "time": elapsed
    }

    if return_stats and return_logs:
        return (None, steps, stats, logs)
    elif return_logs:
        return (None, steps, logs)
    elif return_stats:
        return (None, steps, stats)
    return (None, steps) if return_steps else None
