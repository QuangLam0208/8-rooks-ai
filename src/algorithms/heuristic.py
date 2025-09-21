# h càng nhỏ -> càng tốt

def h_misplaced(state, goal):
    """
    Heuristic = số quân đã đặt nhưng sai cột so với goal.
    - state: đường đi hiện tại
    - goal: nghiệm mong muốn (list)
    """
    return sum(1 for i in range(len(state)) if state[i] != goal[i])

def h_partial(state, goal):
    """
    Heuristic cho state CHƯA ĐẦY ĐỦ:
    - Số quân đã đặt nhưng sai vị trí
    + Số quân còn thiếu
    """
    wrong = sum(1 for i in range(len(state))
                if state[i] != goal[i])
    missing = len(goal) - len(state)
    return wrong + missing