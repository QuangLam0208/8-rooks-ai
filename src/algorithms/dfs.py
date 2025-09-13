def dfs_rooks(n, goal=None):
    """
    DFS đặt n quân xe, trả về tất cả trạng thái duyệt được.
    Nếu goal != None thì dừng đúng tại goal.
    """
    stack = [[]]
    steps = []

    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    while stack:
        state = stack.pop()
        steps.append(state)   # luôn lưu lại bước

        row = len(state)
        if row == n:
            if state == goal:
                return state # chỉ trả về state cuối cùng, nếu muốn trả về các bước thì return steps
            continue

        # mở rộng theo DFS (thêm cuối stack)
        for col in range(n-1, -1, -1):  # duyệt ngược để cùng thứ tự với BFS
            if col not in state:
                stack.append(state + [col])

    return None # nếu muốn trả về các bước thì return steps