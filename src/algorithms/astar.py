import heapq
import time
from .cost import placement_cost_goal
from .heuristic import h_misplaced

def a_star_search(n=8, goal=None, return_steps=False, return_stats=False,
                  placement_cost=placement_cost_goal, heuristic=h_misplaced):
    """
    A* Search cho bài toán 8 quân xe.
    - visited: số trạng thái đã được lấy ra khỏi hàng đợi để xét
    - expanded: tổng số trạng thái con đã được sinh ra
    - frontier: số trạng thái còn lại trong open_list
    """
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    # open_list: (f, g, state)
    open_list = []
    heapq.heappush(open_list, (0, 0, []))  # f=0, g=0, state rỗng
    visited = set()

    steps_visual = []   # từng node pop ra (dùng để animate)
    steps_round  = []   # snapshot toàn bộ open_list mỗi vòng

    expanded_count = 0
    visited_count = 0

    start_time = time.time()

    while open_list:
        # Lưu snapshot open_list trước khi expand
        snapshot = [(f, g, s[:]) for (f, g, s) in open_list]
        steps_round.append(snapshot)

        f, g, state = heapq.heappop(open_list)
        steps_visual.append(state[:])
        visited_count += 1

        row = len(state)
        # Kiểm tra goal
        if row == n:
            if goal is None or state == goal:
                elapsed = (time.time() - start_time) * 1000
                stats = {
                    "expanded": expanded_count,
                    "visited": visited_count,
                    "frontier": len(open_list),
                    "time": elapsed
                }
                if return_stats:
                    if return_steps:
                        return state, steps_visual, stats
                    return state, stats
                if return_steps:
                    return state, steps_visual, steps_round
                return state
            continue

        if tuple(state) in visited:
            continue
        visited.add(tuple(state))

        # Mở rộng node hiện tại
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
                expanded_count += 1

    # Không tìm thấy goal
    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": len(open_list),
        "time": elapsed
    }

    if return_stats:
        if return_steps:
            return None, steps_visual, stats
        return None, stats
    if return_steps:
        return None, steps_visual, steps_round
    return None
