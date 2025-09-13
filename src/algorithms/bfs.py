from collections import deque

def bfs_rooks(n, goal=None):
    """
    BFS đặt n quân xe, trả về state cuối cùng = goal (nếu có).
    """
    from collections import deque
    queue = deque([[]])

    while queue:
        state = queue.popleft()

        row = len(state)
        if row == n:
            if goal is not None and isinstance(goal, tuple):
                goal = list(goal)
            if state == goal:
                return state  # chỉ trả về state cuối cùng, nếu muốn trả về các bước thì return steps
            continue

        # mở rộng
        for col in range(n):
            if col not in state:
                queue.append(state + [col])

    return None # nếu muốn trả về các bước thì return steps