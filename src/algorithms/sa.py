import math, random
from .heuristic import h_misplaced, h_partial

def expand_partial(state, n):
    """
    Sinh các successor bằng cách ĐẶT THÊM 1 QUÂN mới
    vào hàng kế tiếp.
    """
    successors = []
    row = len(state)
    if row < n:
        for col in range(n):
            if col not in state:         # tránh trùng cột
                successors.append(state + [col])
    return successors

def simulated_annealing(n, goal, heuristic=h_partial,
                                max_iter=10000):
    """
    Simulated Annealing đặt từng quân:
    - Bắt đầu từ state rỗng []
    - Mỗi bước chỉ mở rộng thêm 1 quân
    """
    current = []               # bắt đầu rỗng
    best = current[:]          # state tốt nhất
    best_score = heuristic(current, goal)

    t = 1
    for _ in range(max_iter):
        T = max(0.01, 1000 / (t + 1))

        if current == goal:
            return current     # đã đặt đủ và đúng

        successors = expand_partial(current, n)
        if not successors:
            # không còn nước đi hợp lệ
            return best if best_score == 0 else None

        # Tìm successor tốt nhất
        scored = [(heuristic(s, goal), s) for s in successors]
        scored.sort(key=lambda x: x[0])
        best_s_h, best_s = scored[0]

        curr_h = heuristic(current, goal)
        if best_s_h < curr_h:
            current = best_s
        else:
            # chọn ngẫu nhiên 1 successor và xét xác suất
            next_state = random.choice(successors)
            deltaE = curr_h - heuristic(next_state, goal)
            if deltaE > 0:
                current = next_state
            else:
                if random.random() < math.exp(deltaE / T):
                    current = next_state

        # cập nhật state tốt nhất
        score = heuristic(current, goal)
        if score < best_score:
            best = current[:]
            best_score = score

        t += 1

    return best if best_score == 0 else None