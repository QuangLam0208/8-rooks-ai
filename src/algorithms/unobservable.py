import random
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

def dfs_belief_search(n, goal, max_expansions=None):
    if isinstance(goal, tuple):
        goal = list(goal)

    start_time = time.time()
    rand = list(range(n))
    random.shuffle(rand)
    start_belief = [[], [1]]
    goal_beliefs = [
        list(range(n)),
        goal,
        rand
    ]

    stack = [start_belief]
    expanded = 0
    visited = 0

    # visited beliefs: để tránh lặp vô tận (mỗi belief lưu dạng tuple of tuples)
    visited_beliefs = set()

    while stack:
        belief = stack.pop()
        visited += 1
        # tránh xử lý lặp lại cùng belief (AN TOÀN: giảm khả năng đơ)
        key = tuple(tuple(s) for s in belief)
        if key in visited_beliefs:
            # tiếp tục vòng sau, không đổi logic gốc nhiều, chỉ tránh lặp chính xác cùng belief
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
                    return state, stats

            # nếu không có state == goal, return state đầu tiên
            elapsed = (time.time() - start_time) * 1000
            stats = {
                "expanded": expanded,
                "visited": visited,
                "frontier": len(stack),
                "time": elapsed
            }
            return belief[0], stats

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
                    return None, stats

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
    return None, stats

def successors_visual(belife, n, action):
    new_belief = []

    for state in belife:
        # chỉ di chuyển 1 quân ở cuối sang vị trí hợp lệ cùng hàng
        if action == "move":
            if not state or len(state) == n:
                new_belief.append(state)
                continue

            last_col = state[-1]
            for col in range(n):
                if col != last_col and col not in state:
                    new_state = state[:-1] + [col]
                    new_belief.append(new_state)
                    break

        # chỉ đặt thêm 1 quân vào 1 vị trí hợp lệ ở hàng tiếp theo
        if action == "place":
            if len(state) == n:
                new_belief.append(state)
                continue

            for col in range(n):
                if col not in state:
                    new_state = state + [col]
                    new_belief.append(new_state)
                    break        
    
    return new_belief


def dfs_belief_search_visual(n, goal, return_steps=True, return_logs=True, max_expansions=None):
    if isinstance(goal, tuple):
        goal = list(goal)

    start_time = time.time()
    rand = list(range(n))
    random.shuffle(rand)
    start_belief = [[], [1]]
    goal_beliefs = [
        # list(range(n)),
        goal,
        rand
    ]

    stack = [start_belief]
    expanded = 0
    visited = 0
    visited_beliefs = set()

    steps_visual = []
    logs = []
    logs.append(f"Initial belief: {start_belief}")
    steps_visual.append([])
    logs.append(f"Goal belief: {goal_beliefs}")
    steps_visual.append([])
    while stack:
        logs.append(f"Stack: {stack}")
        steps_visual.append([])
        belief = stack.pop()
        visited += 1
        key = tuple(tuple(s) for s in belief)
        steps_visual.append([])
        steps_visual.append(belief[0])
        steps_visual.append(belief[1] if len(belief) == 2 else belief[0])

        if key in visited_beliefs:
            logs.append(f"Skip repeated belief: {belief}")
            continue
        visited_beliefs.add(key)
        logs.append(f"Visiting belief #{visited}: {belief}")

        # Kiểm tra goal
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
                    logs.append(f"Found GOAL state: {state}")
                    if return_steps:
                        if return_logs:
                            return state, steps_visual, logs

            elapsed = (time.time() - start_time) * 1000
            stats = {
                "expanded": expanded,
                "visited": visited,
                "frontier": len(stack),
                "time": elapsed
            }
            logs.append(f"Goal belief found (not exact match): {belief[0]}")
            if return_steps:
                if return_logs:
                    return belief[0], steps_visual, logs

        # sinh belief mới từ move và place
        move_belief = successors_visual(belief, n, action="move")
        if belief[0] != move_belief[0]:
            expanded += 1
        if belief[1] != move_belief[1]:
            expanded += 1
        place_belief = successors_visual(belief, n, action="place")
        if belief[0] != place_belief[0]:
            expanded += 1
        if belief[1] != place_belief[1]:
            expanded += 1

        # Giới hạn mở rộng (nếu có)
        if max_expansions is not None and expanded > max_expansions:
            elapsed = (time.time() - start_time) * 1000
            stats = {
                "expanded": expanded,
                "visited": visited,
                "frontier": len(stack),
                "time": elapsed
            }
            logs.append(f"Max expansion limit reached ({max_expansions}), stop.")
            if return_steps:
                if return_logs:
                    return None, steps_visual, logs
        
        stack.append(move_belief)
        stack.append(place_belief)
        logs.append(f"Push move_belief: {move_belief}")
        logs.append(f"Push place_belief: {place_belief}")

    # Không tìm thấy goal
    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded,
        "visited": visited,
        "frontier": len(stack),
        "time": elapsed
    }
    logs.append("No goal found after full search.")
    if return_steps:
        if return_logs:
            return None, steps_visual, logs