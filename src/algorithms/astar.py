import heapq
from .cost import placement_cost_goal
from .heuristic import h_misplaced

def a_star_search(n=8, goal=None, placement_cost=placement_cost_goal, heuristic=h_misplaced):
    """
    A* Search cho bài toán 8 quân xe.
    - n: kích thước bàn cờ (mặc định 8)
    - goal: trạng thái đích (list hoặc tuple)
    - placement_cost: hàm tính chi phí đặt quân
    - heuristic: hàm heuristic
    """
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    # open_list: (f, g, state)
    open_list = []
    heapq.heappush(open_list, (0, 0, []))  # f=0, g=0, state rỗng
    visited = set()
    steps = []

    while open_list:
        f, g, state = heapq.heappop(open_list)
        steps.append((f, g, state))

        row = len(state)
        # Nếu đã đặt đủ n quân
        if row == n:
            if goal is None or state == goal:
                return state  # trả về nghiệm
            continue

        if tuple(state) in visited:
            continue
        visited.add(tuple(state))

        for col in range(n):
            if col not in state:  # không trùng cột
                # g(n+1): chi phí thực tế
                step_cost = placement_cost(state, row, col, goal) if placement_cost else 1
                new_g = g + step_cost
                new_state = state + [col]

                # h(n+1): heuristic
                new_h = heuristic(new_state, goal) if heuristic and goal else (n - len(new_state))

                # f = g + h
                new_f = new_g + new_h
                heapq.heappush(open_list, (new_f, new_g, new_state))

    return None
