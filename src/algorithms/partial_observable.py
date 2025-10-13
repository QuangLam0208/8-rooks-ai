import time

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


def dfs_partial_obs(n, goal, prefix_len=6, return_steps=False, return_stats=False, max_expansions=None):
    """
    DFS trong môi trường quan sát một phần (Partial Observable)
    ✅ Giữ nguyên logic gốc
    ➕ Thêm thống kê expanded, visited, frontier, time
    ➕ Thêm visited_beliefs để tránh lặp vô hạn
    """
    if isinstance(goal, tuple):
        goal = list(goal)

    start_time = time.time()

    # ===== Khởi tạo belief ban đầu =====
    prefix = goal[:prefix_len]

    for col in range(n):
        if col not in prefix:
            start_belief2 = prefix + [col]
            break
    belief_start = [prefix, start_belief2]

    # goal beliefs (chỉ để mỗi goal để dễ đạt kết quả)
    goal_beliefs = [goal]

    stack = [belief_start]
    steps = [] if return_steps else None

    expanded = 0
    visited = 0
    visited_beliefs = set()  # tránh lặp vô hạn

    while stack:
        belief = stack.pop()
        visited += 1

        if return_steps:
            steps.append([s[:] for s in belief])

        # tránh lặp lại cùng belief
        key = tuple(tuple(s) for s in belief)
        if key in visited_beliefs:
            continue
        visited_beliefs.add(key)

        # ===== Kiểm tra goal =====
        if all(state in goal_beliefs for state in belief):
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
            # nếu không có state == goal, trả về state đầu
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

        # ===== Sinh belief mới =====
        move_belief, place_belief = [], []
        for state in belief:
            for ns in successors_partial(state, n, prefix_len):
                if len(ns) == len(state):  # move
                    move_belief.append(ns)
                else:                      # place
                    place_belief.append(ns)
                expanded += 1

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

    # ===== Không tìm thấy goal =====
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
