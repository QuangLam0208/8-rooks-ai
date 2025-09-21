import heapq
from .cost import placement_cost_goal

def uniform_cost_search(n, goal, placement_cost_goal=placement_cost_goal):
    if isinstance(goal, tuple):
        goal = list(goal)

    heap = [(0, [])] # (chi phí, state)
    visited = set()
    steps = []

    while heap:
        cost, state = heapq.heappop(heap)
        steps.append((cost, state))

        row = len(state)
        if row == n:
            if state == goal:
                return state # chỉ trả về goal (nếu muốn trả các bước thì return steps)
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

    return None # nếu muốn trả về danh sách các state thì return steps