from collections import deque

def bfs_rooks(n, goal=None):
    """
    BFS đặt n quân xe, trả về tất cả trạng thái duyệt được.
    Nếu goal != None thì dừng đúng tại goal.
    """
    queue = deque([[]])  
    steps = []  

    while queue:
        state = queue.popleft()
        steps.append(state)

        row = len(state)
        if row == n:
            if goal is not None and isinstance(goal, tuple):
                goal = list(goal)
            if state == goal:
                return steps  # Dừng ngay khi khớp goal
            continue  # nếu khác goal thì bỏ qua

        # mở rộng
        for col in range(n):
            if col not in state:
                queue.append(state + [col])

    return steps
