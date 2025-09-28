from .heuristic import h_misplaced, h_partial

def hill_climbing(n, goal, return_steps=False, heuristic=h_partial):
    current = []  # bắt đầu từ state rỗng
    steps_visual = []
    steps_console = []
    iter_count = 1

    # Đảm bảo goal là list
    goal = list(goal) if isinstance(goal, tuple) else goal

    while True:
        # Lưu lại trạng thái hiện tại
        if return_steps:
            h_curr = heuristic(current, goal)
            steps_visual.append(current[:])           # copy để tránh mutate
            steps_console.append((iter_count, current[:], h_curr))

        row = len(current)
        if row == n:
            if return_steps:
                return (current if current == goal else None,
                        steps_visual, steps_console)
            return current if current == goal else None

        # Sinh tất cả con
        candidates = []
        for col in range(n):
            if col not in current:
                next_state = current + [col]
                candidates.append((heuristic(next_state, goal), next_state))

        if not candidates:
            if return_steps:
                return None, steps_visual, steps_console
            return None  # hết đường đi

        # Chọn child tốt nhất (có thể bằng hoặc tốt hơn)
        best_h, best_state = min(candidates, key=lambda x: x[0])

        # Nếu không cải thiện -> dừng
        curr_h = heuristic(current, goal)
        if best_h >= curr_h:
            if return_steps:
                return None, steps_visual, steps_console
            return None

        # Di chuyển đến child tốt nhất
        current = best_state
        iter_count += 1