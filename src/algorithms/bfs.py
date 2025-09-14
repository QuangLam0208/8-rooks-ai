from collections import deque

def breadth_first_search(n, goal=None):
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
                return state  # chỉ trả về state cuối cùng, nếu muốn trả về các bước thì return steps
            continue  # nếu khác goal thì bỏ qua

        # mở rộng
        for col in range(n):
            if col not in state:
                queue.append(state + [col])

    return None # nếu muốn trả về các bước thì return steps