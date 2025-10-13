import time

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


def dfs_belief_search(n, goal, return_steps=False, return_stats=False, max_expansions=None):
    """
    DFS with belief (Unobservable) — giữ nguyên logic gốc, thêm options:
      - return_steps: nếu True trả về (result, steps)
      - return_stats: nếu True trả về (result, steps?, stats)
    Trả về theo chuẩn project:
      - nếu return_stats and return_steps: (result, steps, stats)
      - nếu return_stats and not return_steps: (result, stats)
      - nếu not return_stats and return_steps: (result, steps)
      - nếu none: result
    Chú ý: thêm visited_beliefs để tránh lặp vô tận; max_expansions để phòng khi chạy quá lâu.
    """
    if isinstance(goal, tuple):
        goal = list(goal)

    start_time = time.time()

    # (GIỮ NGUYÊN) cấu hình đầu
    start_belief = [[], [5]]
    goal_beliefs = [
        [0,1,2,3,4,5,6,7],
        goal,              # goal truyền vào
        [0,3,2,1,4,5,7,6]
    ]

    stack = [start_belief]
    steps = [] if return_steps else None

    expanded = 0
    visited = 0

    # visited beliefs: để tránh lặp vô tận (mỗi belief lưu dạng tuple of tuples)
    visited_beliefs = set()

    while stack:
        belief = stack.pop()

        # lưu steps chỉ khi user yêu cầu (tránh chiếm memory)
        if return_steps:
            steps.append([s[:] for s in belief])

        visited += 1

        # tránh xử lý lặp lại cùng belief (AN TOÀN: giảm khả năng đơ)
        key = tuple(tuple(s) for s in belief)
        if key in visited_beliefs:
            # tiếp tục vòng sau
            # NOTE: không đổi logic gốc nhiều, chỉ tránh lặp chính xác cùng belief
            continue
        visited_beliefs.add(key)

        # kiểm tra nếu toàn bộ state trong belief thuộc goal_beliefs
        if all(state in goal_beliefs for state in belief):
            # ưu tiên nếu có state == goal
            for state in belief:
                if state == goal:
                    elapsed = (time.time() - start_time) * 1000
                    stats = {
                        "expanded": expanded,
                        "visited": visited,
                        "frontier": len(stack),
                        "time": elapsed
                    }
                    if return_stats:
                        if return_steps:
                            return state, steps, stats
                        return state, stats
                    if return_steps:
                        return state, steps
                    return state
            # nếu không có state == goal, return state đầu tiên
            elapsed = (time.time() - start_time) * 1000
            stats = {
                "expanded": expanded,
                "visited": visited,
                "frontier": len(stack),
                "time": elapsed
            }
            if return_stats:
                if return_steps:
                    return belief[0], steps, stats
                return belief[0], stats
            if return_steps:
                return belief[0], steps
            return belief[0]

        # sinh belief mới từ move và place
        move_belief = []
        place_belief = []
        for state in belief:
            for ns in successors(state, n):
                if len(ns) == len(state):   # move
                    move_belief.append(ns)
                else:                       # place
                    place_belief.append(ns)
                expanded += 1

                # an toàn: nếu có giới hạn expansions và vượt qua thì dừng để tránh treo
                if max_expansions is not None and expanded > max_expansions:
                    elapsed = (time.time() - start_time) * 1000
                    stats = {
                        "expanded": expanded,
                        "visited": visited,
                        "frontier": len(stack),
                        "time": elapsed
                    }
                    if return_stats:
                        if return_steps:
                            return None, steps, stats
                        return None, stats
                    if return_steps:
                        return None, steps
                    return None

        if move_belief:
            stack.append(move_belief)
        if place_belief:
            stack.append(place_belief)

    # Không tìm thấy goal
    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded,
        "visited": visited,
        "frontier": len(stack),
        "time": elapsed
    }

    if return_stats:
        if return_steps:
            return None, steps, stats
        return None, stats
    if return_steps:
        return None, steps
    return None
