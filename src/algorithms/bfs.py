from collections import deque

def bfs_rooks(n):
    """Tìm nghiệm đặt n quân xe bằng BFS"""
    queue = deque([[]])  # trạng thái ban đầu: chưa có xe nào
    solutions = []

    while queue:
        state = queue.popleft()

        row = len(state)
        if row == n:
            return state  # nghiệm đầy đủ

        for col in range(n):
            if col not in state:  # đảm bảo không trùng cột
                queue.append(state + [col])

    return None
