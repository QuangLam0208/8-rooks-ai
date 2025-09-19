import math
import random

def random_successor(state, n):
    """
    Sinh ngẫu nhiên 1 successor từ state.
    Cách làm: chọn 1 hàng bất kỳ và đổi cột của nó sang 1 vị trí khác.
    """
    if not state:  # nếu state rỗng
        # khởi tạo 1 trạng thái ngẫu nhiên
        return [random.randrange(n) for _ in range(n)]

    next_state = state.copy()
    row = random.randrange(n)
    col = random.randrange(n)
    next_state[row] = col
    return next_state

def all_successors(state, n):
    """
    Sinh tất cả các successor từ state hiện tại bằng cách thay đổi 1 hàng sang cột khác
    """
    successors = []
    for row in range(n):
        for col in range(n):
            if state[row] != col:
                next_state = state.copy()
                next_state[row] = col
                successors.append(next_state)
    return successors

def simulated_annealing(n, goal, heuristic, max_iter=10000):
    """
    Nếu có successor tốt nhất hơn current -> chọn nó
    Nếu không -> random 1 successor và xét theo xác suất SA.

    Thuật toán Simulated Annealing cho n quân xe.
    - n: kích thước bàn cờ
    - goal: trạng thái đích
    - heuristic: hàm đánh giá
    - max_iter: số vòng lặp tối đa
    """
    current = [random.randrange(n) for _ in range(n)]
    best = current.copy()  # lưu lại state tốt nhất tìm được
    best_score = heuristic(current, goal)

    t = 1
    for _ in range(max_iter):
        T = max(0.01, 1000 / (t + 1))

        if current == goal:
            return current  # tìm thấy goal
        
        successors = all_successors(current, n) # tất cả successor của current

        # Tìm successor tốt nhất
        scored = [(heuristic(s, goal), s) for s in successors]
        scored.sort(key=lambda x: x[0])  # sắp xếp theo h tăng dần
        best_successor_score, best_successor = scored[0]
        
        if best_successor_score < heuristic(current, goal):
            current = best_successor
        else:
            next_state = random.choice(successors)
            deltaE = heuristic(current, goal) - heuristic(next_state, goal)

            if deltaE > 0:
                current = next_state
            else:
                if random.random() < math.exp(deltaE / T):
                    current = next_state

        # cập nhật state tốt nhất
        score = heuristic(current, goal)
        if score < best_score:
            best = current.copy()
            best_score = score

        t += 1

    return best