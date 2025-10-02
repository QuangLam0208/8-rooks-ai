def successors_partial(state, n, prefix_len):
    """
    Sinh ra 1 move hợp lệ và 1 place hợp lệ từ state.
    - state: trạng thái hiện tại (list các cột đã đặt).
    - n: kích thước bàn cờ.
    - prefix_len: số hàng đầu đã biết (không được thay đổi).
    """
    successors = []
    row = len(state)

    # move (chỉ cho các quân sau prefix)
    if row > prefix_len:
        for r in range(prefix_len, row):
            for col in range(n):
                if col != state[r] and col not in state:
                    new_state = state.copy()
                    new_state[r] = col
                    successors.append(new_state)
                    break
            if successors:
                break

    # place (nếu chưa đủ n quân)
    if row < n:
        for col in range(n):
            if col not in state:
                successors.append(state + [col])
                break

    return successors


def dfs_partial_obs(n, goal, prefix_len=6, return_steps=False):
    """
    DFS trong môi trường quan sát một phần.
    - Start belief = {prefix, prefix + [1 quân tiếp theo]}.
    - Goal beliefs = {goal, 2 state khác full nhưng có prefix đúng như goal}.
    - Điều kiện dừng: tất cả state trong belief nằm trong goal_beliefs.
    """
    prefix = goal[:prefix_len]

    for col in range(n):
        if col not in prefix:
            start_belief2 = prefix + [col]
            break
    belief_start = [prefix, start_belief2]

    goal2 = prefix
    for col in range(n):
        if col not in goal2:
            goal2 += [col]

    # goal beliefs (ví dụ gồm 3 state)
    goal_beliefs = [
        goal
    ]

    stack = [belief_start]
    steps = []

    while stack:
        belief = stack.pop()
        steps.append(belief)

        # check goal: tất cả state trong belief thuộc goal_beliefs
        if all(state in goal_beliefs for state in belief):
            for state in belief:
                if state == goal:
                    return (state, steps) if return_steps else state
            return (belief[0], steps) if return_steps else belief[0]

        # sinh belief mới
        move_belief, place_belief = [], []
        for state in belief:
            for ns in successors_partial(state, n, prefix_len):
                if len(ns) == len(state):  # move
                    move_belief.append(ns)
                else:                      # place
                    place_belief.append(ns)

        if move_belief:
            stack.append(move_belief)
        if place_belief:
            stack.append(place_belief)

    return (None, steps) if return_steps else None
