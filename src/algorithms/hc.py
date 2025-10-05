import time
from .heuristic import h_partial

def hill_climbing(n, goal, return_steps=False, return_stats=False, heuristic=h_partial):
    """
    Hill Climbing đặt từng quân.
    - expanded: số trạng thái con được sinh ra
    - visited: số trạng thái đã được xét (đã chọn)
    - frontier: = 0 (vì không lưu trạng thái chờ)
    """
    start_time = time.time()
    goal = list(goal) if isinstance(goal, tuple) else goal

    current = []  # bắt đầu từ state rỗng
    steps_visual = []
    steps_console = []

    expanded_count = 0
    visited_count = 0
    iter_count = 1

    while True:
        if return_steps:
            h_curr = heuristic(current, goal)
            steps_visual.append(current[:])
            steps_console.append((iter_count, current[:], h_curr))

        visited_count += 1
        row = len(current)

        # Nếu đủ n quân -> kiểm tra goal
        if row == n:
            elapsed = (time.time() - start_time) * 1000
            stats = {
                "expanded": expanded_count,
                "visited": visited_count,
                "frontier": 0,
                "time": elapsed
            }
            if return_stats:
                if return_steps:
                    return (current if current == goal else None), steps_visual, stats
                return (current if current == goal else None), stats
            if return_steps:
                return (current if current == goal else None), steps_visual, steps_console
            return current if current == goal else None

        # Sinh tất cả con hợp lệ
        candidates = []
        for col in range(n):
            if col not in current:
                next_state = current + [col]
                candidates.append((heuristic(next_state, goal), next_state))
                expanded_count += 1

        if not candidates:
            break  # không còn nước đi

        best_h, best_state = min(candidates, key=lambda x: x[0])
        curr_h = heuristic(current, goal)

        # Nếu không cải thiện -> dừng
        if best_h >= curr_h:
            break

        # Di chuyển đến child tốt nhất
        current = best_state
        iter_count += 1

    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": 0,
        "time": elapsed
    }

    if return_stats:
        if return_steps:
            return None, steps_visual, stats
        return None, stats
    if return_steps:
        return None, steps_visual, steps_console
    return None
