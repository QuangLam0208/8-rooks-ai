from collections import deque
import heapq

def placement_cost_goal(state, row, col, goal):
    '''
    Tính chi phí đặt quân ở (row, col) so với trạng thái đích goal.
    state: danh sách các cột đã đặt
    row: hàng hiện tại
    col: cột hiện tại
    goal: trạng thái đích dạng list
    '''

    if goal is None:
        return 1
    
    target_col = goal[row]
    if col == target_col:
        return 1
    else:
        return abs(col - target_col) + 1
    
def ucs_rooks_goal(n, goal):
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