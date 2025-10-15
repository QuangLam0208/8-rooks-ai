import time

def forward_checking_search(n, goal=None, max_expansions=None):
    # Chuẩn hóa goal
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

    def forward_check(state, domains):
        nonlocal expanded, visited
        visited += 1

        # Nếu đạt goal
        if len(state) == n:
            if goal_list is not None:
                if state == goal_list:
                    return state
                return None
            else:
                return state

        row = len(state)
        for col in list(domains[row]):  # snapshot để tránh modify khi lặp
            if col not in state:
                expanded += 1
                if max_expansions is not None and expanded > max_expansions:
                    return None

                # Cập nhật miền giá trị cho các hàng tiếp theo
                new_domains = [d[:] for d in domains]
                for r in range(row + 1, n):
                    if col in new_domains[r]:
                        new_domains[r].remove(col)

                # Nếu tất cả hàng còn lại vẫn còn miền hợp lệ thì tiếp tục
                if all(len(d) > 0 for r, d in enumerate(new_domains) if r > row):
                    result = forward_check(state + [col], new_domains)
                    if result is not None:
                        return result

        return None

    domains = [list(range(n)) for _ in range(n)]
    res = forward_check([], domains)

    elapsed = (time.time() - start_time) * 1000  # ms
    stats = {
        "expanded": expanded,
        "visited": visited,
        "frontier": 0,   # frontier không áp dụng trong forward checking
        "time": elapsed
    }

    return res, stats

def forward_checking_search_visual(n, goal=None, return_steps=False, return_logs=False, max_expansions=None):
    # Chuẩn hóa goal
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
    steps_visual = []
    logs = []
    found_result = None

    def add_step(state, message, depth=0):
        indent = "   " * depth
        logs.append(f"{indent}{message}")
        steps_visual.append(state[:])

    def forward_check(state, domains, depth=0):
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

        row = len(state)
        for col in list(domains[row]):  # snapshot để tránh modify khi lặp
            if col not in state:
                expanded += 1
                add_step(state, f"→ Try placing at row {row}, column {col}", depth)

                if max_expansions is not None and expanded > max_expansions:
                    add_step(state, f"  Expansion limit reached ({max_expansions}), stop.", depth)
                    return None

                # Cập nhật miền giá trị cho các hàng tiếp theo
                new_domains = [d[:] for d in domains]
                for r in range(row + 1, n):
                    if col in new_domains[r]:
                        new_domains[r].remove(col)

                # Kiểm tra nếu tất cả hàng còn lại có miền hợp lệ
                if all(len(d) > 0 for r, d in enumerate(new_domains) if r > row):
                    result = forward_check(state + [col], new_domains, depth + 1)
                    if result is not None:
                        return result
                else:
                    add_step(state, f"  Domain wipeout at row {row+1}, backtrack.", depth)

                add_step(state, f"  Backtrack from {state + [col]}", depth)

        add_step(state, f"No valid move from {state}, return None", depth)
        return None

    # Bắt đầu với miền ban đầu: mỗi hàng có thể chọn bất kỳ cột nào
    domains = [list(range(n)) for _ in range(n)]
    result = forward_check([], domains)

    elapsed = (time.time() - start_time) * 1000  # ms
    stats = {
        "expanded": expanded,
        "visited": visited,
        "frontier": 0,
        "time": elapsed
    }

    if result is None:
        add_step([], "  No solution found.")
    else:
        add_step(result, f"  Finished. Result: {result}")

    if return_steps and return_logs:
        return result, steps_visual, logs
    elif return_steps:
        return result, steps_visual
    elif return_logs:
        return result, logs
    else:
        return result
