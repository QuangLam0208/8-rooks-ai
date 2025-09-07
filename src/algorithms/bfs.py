from collections import deque

def bfs_rooks(n):
    """Tìm nghiệm đặt n quân xe bằng BFS, trả về tất cả các bước"""
    queue = deque([[]])  # trạng thái ban đầu
    steps = []  # lưu các bước

    while queue:
        state = queue.popleft()
        steps.append(state)  # lưu lại trạng thái hiện tại

        row = len(state)
        if row == n:  # đã đủ n quân xe
            return steps  

        for col in range(n):
            if col not in state:  # đảm bảo không trùng cột
                queue.append(state + [col])

    return steps
