import time

def depth_first_search(n, goal=None, return_steps=False, return_stats=False):
    """
    DFS đặt n quân xe.
    - visited: số trạng thái đã được xét (được lấy ra khỏi stack)
    - expanded: tổng số trạng thái con đã được sinh ra (thêm vào stack)
    - frontier: số trạng thái còn lại trong stack
    """
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
                if return_stats:
                    return (state, steps, stats)
                return (state, steps) if return_steps else state
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

    if return_stats:
        return (None, steps, stats)
    return (None, steps) if return_steps else None
