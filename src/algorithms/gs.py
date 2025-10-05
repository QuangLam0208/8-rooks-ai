import heapq
import time
from .heuristic import h_misplaced

def greedy_best_search(n=8, goal=None, return_steps=False, return_stats=False, heuristic=h_misplaced):
    """
    Greedy Best-First Search cho bài toán 8 quân xe.
    - visited: số trạng thái đã được lấy ra khỏi hàng đợi để xét
    - expanded: tổng số trạng thái con đã được sinh ra
    - frontier: số trạng thái còn lại trong open_list
    """
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    start_time = time.time()

    open_list = []
    steps_visual = []   # các state được pop ra (dùng để animate)
    steps_round  = []   # snapshot mỗi vòng lặp
    visited = set()

    expanded_count = 0
    visited_count = 0

    # trạng thái ban đầu
    h0 = heuristic([], goal) if heuristic and goal else (n - 0)
    heapq.heappush(open_list, (h0, []))

    while open_list:
        # lưu snapshot trước khi mở rộng
        snapshot = [(h, s[:]) for (h, s) in open_list]
        steps_round.append(snapshot)

        h, state = heapq.heappop(open_list)
        steps_visual.append(state)
        visited_count += 1

        # kiểm tra goal
        if len(state) == n:
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

        # mở rộng node hiện tại
        row = len(state)
        for col in range(n):
            if col not in state:
                new_state = state + [col]
                new_h = heuristic(new_state, goal) if heuristic and goal else (n - len(new_state))
                heapq.heappush(open_list, (new_h, new_state))
                expanded_count += 1

    # không tìm thấy lời giải
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
