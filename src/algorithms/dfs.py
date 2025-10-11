import time

def depth_first_search(n, goal=None):
    start_time = time.time()
    stack = [[]]
    steps = []
    visited_count = 0
    expanded_count = 0

    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    while stack:
        state = stack.pop()
        visited_count += 1
        steps.append(state)

        row = len(state)
        if row == n:
            if state == goal:
                elapsed = (time.time() - start_time) * 1000
                stats = {
                    "expanded": expanded_count,
                    "visited": visited_count,
                    "frontier": len(stack),
                    "time": elapsed
                }
                return (state, steps, stats)
            continue

        # mở rộng node hiện tại theo DFS
        for col in range(n - 1, -1, -1):  # duyệt ngược để cùng thứ tự với BFS
            if col not in state:
                new_state = state + [col]
                stack.append(new_state)
                expanded_count += 1

    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": len(stack),
        "time": elapsed
    }
    return (None, steps, stats)
    
def depth_first_search_visual(n, goal=None, return_steps=False, return_stats=False, return_logs=False):
    """
    DFS đặt n quân xe, có log chi tiết cho Visualization.
    - return_logs: nếu True, trả về danh sách log từng bước.
    """
    start_time = time.time()
    stack = [[]]
    steps = []
    logs = []
    visited_count = 0
    expanded_count = 0

    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    while stack:
        state = stack.pop()
        visited_count += 1
        steps.append(state)

        # Ghi log state hiện tại + stack hiện tại
        stack_snapshot = list(stack)
        logs.append(f"State {visited_count - 1}: {state} | Stack: {stack_snapshot}")

        row = len(state)
        if row == n:
            if state == goal:
                elapsed = (time.time() - start_time) * 1000
                stats = {
                    "expanded": expanded_count,
                    "visited": visited_count,
                    "frontier": len(stack),
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

        # Mở rộng node hiện tại (theo DFS: duyệt ngược để thứ tự khớp với BFS)
        for col in range(n - 1, -1, -1):
            if col not in state:
                new_state = state + [col]
                stack.append(new_state)
                expanded_count += 1

    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": len(stack),
        "time": elapsed
    }

    if return_stats and return_logs:
        return (None, steps, stats, logs)
    elif return_logs:
        return (None, steps, logs)
    elif return_stats:
        return (None, steps, stats)
    return (None, steps) if return_steps else None
