def successors(state, n):
    successors = []
    row = len(state)

    # move
    if state:
        for r in range(row):
            for col in range(n):
                if col != state[r] and col not in state:
                    new_state = state.copy()
                    new_state[r] = col
                    successors.append(new_state)
                    break
            if successors:
                break

    # place
    if row < n:
        for col in range(n):
            if col not in state:
                successors.append(state + [col])
                break
    
    return successors


def dfs_belief_search(n, goal, return_steps=False):
    """
    DFS với belief = tập các state
    - start belief = {[], [5]}
    - goal_beliefs = {[0..7], [goal], [8 con bất kỳ]}
    """
    start_belief = [[], [5]]
    goal_beliefs = [
        [0,1,2,3,4,5,6,7],
        goal,              # goal truyền vào
        [0,3,2,1,4,5,7,6]
    ]

    stack = [start_belief]
    steps = []

    while stack:
        belief = stack.pop()
        steps.append(belief)

        # kiểm tra nếu toàn bộ state trong belief thuộc goal_beliefs
        if all(state in goal_beliefs for state in belief):
            # ưu tiên nếu có state == goal
            for state in belief:
                if state == goal:
                    return (state, steps) if return_steps else state
            # nếu không có state == goal, return state đầu tiên
            return (belief[0], steps) if return_steps else belief[0]

        # sinh belief mới từ move và place
        move_belief = []
        place_belief = []
        for state in belief:
            for ns in successors(state, n):
                if len(ns) == len(state):   # move
                    move_belief.append(ns)
                else:                       # place
                    place_belief.append(ns)

        if move_belief:
            stack.append(move_belief)
        if place_belief:
            stack.append(place_belief)

    return (None, steps) if return_steps else None
