import heapq
import time
from .cost import placement_cost_goal

def uniform_cost_search(n, goal, return_steps=False, return_stats=False, placement_cost_goal=placement_cost_goal):
    """
    Uniform Cost Search (UCS)
    - visited: số trạng thái đã được lấy ra khỏi hàng đợi để xét
    - expanded: tổng số trạng thái con đã được sinh ra
    - frontier: số trạng thái còn lại trong hàng đợi (heap)
    """
    if isinstance(goal, tuple):
        goal = list(goal)

    start_time = time.time()

    heap = [(0, [])]  # (chi phí, state)
    visited = set()
    steps_visual = []   # Các state được pop ra (dùng để animate)
    steps_round  = []   # Snapshot toàn bộ heap sau mỗi vòng (dùng để in console)

    expanded_count = 0
    visited_count = 0

    while heap:
        cost, state = heapq.heappop(heap)
        steps_visual.append(state)
        visited_count += 1

        row = len(state)
        if row == n:
            if state == goal:
                elapsed = (time.time() - start_time) * 1000
                stats = {
                    "expanded": expanded_count,
                    "visited": visited_count,
                    "frontier": len(heap),
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
            if col not in state:
                step_cost = placement_cost_goal(state, row, col, goal)
                new_cost = cost + step_cost
                new_state = state + [col]
                heapq.heappush(heap, (new_cost, new_state))
                expanded_count += 1

        # Lưu snapshot heap sau mỗi vòng
        steps_round.append(list(heap))

    # Không tìm thấy lời giải
    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": len(heap),
        "time": elapsed
    }

    if return_stats:
        if return_steps:
            return None, steps_visual, stats
        return None, stats
    if return_steps:
        return None, steps_visual, steps_round
    return None
