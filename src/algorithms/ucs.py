import heapq
from .cost import placement_cost_goal

def uniform_cost_search(n, goal, return_steps=False, placement_cost_goal=placement_cost_goal):
    if isinstance(goal, tuple):
        goal = list(goal)

    heap = [(0, [])] # (chi phí, state)
    visited = set()
    steps_visual = []   # Các state được pop ra (dùng để animate)
    steps_round  = []   # Snapshot toàn bộ heap sau mỗi vòng (dùng để print console)

    while heap:
        cost, state = heapq.heappop(heap)
        steps_visual.append(state)

        row = len(state)
        if row == n:
            if state == goal:
                if return_steps:
                    return state, steps_visual, steps_round
                return state
            continue

        if tuple(state) in visited:
            continue
        visited.add(tuple(state))

        for col in range(n):
            if col not in state:
                step_cost = placement_cost_goal(state, row, col, goal)
                new_cost = cost + step_cost
                new_state = state + [col]
                heapq.heappush(heap, (new_cost, new_state))

        # Lưu snapshot toàn bộ hàng đợi hiện tại để in console
        steps_round.append(list(heap))

    if return_steps:
        return None, steps_visual, steps_round
    return None