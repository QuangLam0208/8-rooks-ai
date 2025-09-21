def hill_climbing(n, goal, heuristic):
    current = []  # bắt đầu từ state rỗng
    while True:
        row = len(current)
        if row == n:
            return current if current == list(goal) else None

        # Sinh tất cả con
        candidates = []
        for col in range(n):
            if col not in current:
                next_state = current + [col]
                candidates.append((heuristic(next_state, goal), next_state))

        if not candidates:
            return None  # hết đường đi

        # Chọn child tốt nhất (có thể bằng hoặc tốt hơn)
        best_h, best_state = min(candidates, key=lambda x: x[0])
        current = best_state