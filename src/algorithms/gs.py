import heapq

def greedy_search(n=8, goal=None, heuristic=None):
    """
    Greedy Best-First Search cho bài toán 8 quân xe.
    Nếu goal != None thì dùng heuristic theo goal.
    """
    open_list = []
    steps = []

    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    # start
    h0 = heuristic([], goal) if heuristic and goal else (n - 0)
    heapq.heappush(open_list, (h0, []))

    while open_list:
        h, state = heapq.heappop(open_list)
        steps.append(state)

        # Goal test
        if len(state) == n:
            if goal is None:
                return state
            if state == goal:
                return state
            continue

        row = len(state)
        for col in range(n):
            if col not in state:
                new_state = state + [col]
                new_h = heuristic(new_state, goal) if heuristic and goal else (n - len(new_state))
                heapq.heappush(open_list, (new_h, new_state))

    return None
