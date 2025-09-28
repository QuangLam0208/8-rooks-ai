def depth_first_search(n, goal=None, return_steps=False):
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
                return (state, steps) if return_steps else state
            continue

        # mở rộng theo DFS (thêm cuối stack)
        for col in range(n-1, -1, -1):  # duyệt ngược để cùng thứ tự với BFS
            if col not in state:
                stack.append(state + [col])

    return (None, steps) if return_steps else None # nếu muốn trả về các bước thì return steps