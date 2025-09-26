import random
from .heuristic import h_misplaced, h_partial

def successors(state, n):
    """
    Sinh các successor của 1 state.
    - State là hoán vị: state[i] = cột đặt quân ở hàng i.
    - Successor = đổi cột của 1 hàng sang 1 vị trí khác.
    """
    succ = []
    for i in range(n):
        for j in range(n):
            if j != state[i]:
                s = state[:]
                s[i] = j
                succ.append(s)
    return succ

def beam_search(n, goal, beam_width=10, max_steps=1000, heuristic=h_misplaced):
    """
    Beam Search với heuristic (h càng nhỏ càng tốt).
    - n: kích thước bàn cờ
    - goal: trạng thái đích (list)
    - beam_width: số lượng state tốt nhất giữ lại mỗi vòng
    - max_steps: giới hạn số vòng lặp
    - heuristic: hàm h(state, goal) (giá trị càng nhỏ càng tốt)
    """
    # 1. Khởi tạo beam ban đầu (ngẫu nhiên k state)
    beam = [random.sample(range(n), n) for _ in range(beam_width)]

    for step in range(1, max_steps + 1):
        # Kiểm tra goal
        for s in beam:
            if s == goal:
                # print(f"Goal found at step {step}: {s}")
                return s

        # 2. Sinh toàn bộ successor từ beam hiện tại
        all_succ = []
        for s in beam:
            all_succ.extend(successors(s, n))

        if not all_succ:
            break

        # 3. Chọn beam_width state tốt nhất theo heuristic (nhỏ nhất)
        beam = sorted(all_succ, key=lambda s: heuristic(s, goal))[:beam_width]

    # Hết vòng lặp mà chưa gặp goal
    best = min(beam, key=lambda s: heuristic(s, goal))
    print(f"No exact goal after {max_steps} steps.")
    print(f"Best found: {best} (h={heuristic(best, goal)})")
    return best