import time

def backtracking_search(n, goal=None, max_expansions=None):
    if goal is not None:
        try:
            goal_list = list(goal)
        except TypeError:
            goal_list = None
    else:
        goal_list = None

    start_time = time.time()
    expanded = 0
    visited = 0

    found_result = None

    def backtrack(state):
        nonlocal expanded, visited, found_result
        visited += 1

        # nếu đạt goal
        if len(state) == n:
            if goal_list is not None:
                if state == goal_list:
                    found_result = state
                    return state
                return None
            else:
                found_result = state
                return state

        # sinh tiếp các nhánh hợp lệ
        for col in range(n):
            if col not in state:
                expanded += 1
                if max_expansions is not None and expanded > max_expansions:
                    return None
                result = backtrack(state + [col])
                if result is not None:
                    return result

        return None

    res = backtrack([])

    elapsed = (time.time() - start_time) * 1000  # ms
    stats = {
        "expanded": expanded,
        "visited": visited,
        "frontier": 0,   # frontier không có ý nghĩa rõ ràng trong backtracking (stack đệ quy)
        "time": elapsed
    }
    return res, stats

def backtracking_search_visual(n, goal=None, return_steps=False, return_logs=False, max_expansions=None):
    if goal is not None:
        try:
            goal_list = list(goal)
        except TypeError:
            goal_list = None
    else:
        goal_list = None

    start_time = time.time()
    expanded = 0
    visited = 0
    found_result = None

    steps_visual = []  # mỗi log tương ứng 1 state
    logs = []          # mô tả từng bước

    def add_step(state, message, depth=0):
        """Tiện ích: thêm log và state đồng bộ"""
        indent = "   " * depth
        logs.append(f"{indent}{message}")
        steps_visual.append(state[:])

    def backtrack(state, depth=0):
        nonlocal expanded, visited, found_result
        visited += 1

        add_step(state, f"Visit state: {state}", depth)

        # Nếu đạt goal
        if len(state) == n:
            if goal_list is not None:
                if state == goal_list:
                    found_result = state
                    add_step(state, f"Found GOAL: {state}", depth)
                    return state
                else:
                    add_step(state, f"Reached leaf {state}, not goal.", depth)
                    return None
            else:
                found_result = state
                add_step(state, f"Found valid full state: {state}", depth)
                return state

        # Sinh các nhánh hợp lệ
        for col in range(n):
            if col not in state:
                expanded += 1
                add_step(state, f"→ Try placing at column {col}", depth)
                if max_expansions is not None and expanded > max_expansions:
                    add_step(state, f"⚠️ Expansion limit reached ({max_expansions}), stop.", depth)
                    return None

                result = backtrack(state + [col], depth + 1)
                if result is not None:
                    return result  # stop at first found

                add_step(state, f"← Backtrack from {state + [col]}", depth)

        add_step(state, f"No valid move from {state}, return None", depth)
        return None

    # Gọi đệ quy từ trạng thái rỗng
    result = backtrack([])

    elapsed = (time.time() - start_time) * 1000  # ms
    stats = {
        "expanded": expanded,
        "visited": visited,
        "frontier": 0,
        "time": elapsed
    }

    if result is None:
        add_step([], "No solution found.")
    else:
        add_step(result, f"Finished. Result: {result}")

    if return_steps and return_logs:
        return result, steps_visual, logs
    elif return_steps:
        return result, steps_visual
    elif return_logs:
        return result, logs
    else:
        return result