import time

def depth_limited_search(n, goal=None, limit=None):
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    if limit is None:
        limit = n

    steps_visual = [] 
    expanded_count = 0
    visited_count = 0

    start_time = time.time()

    def recursive_dls(state, depth, frontier):
        nonlocal expanded_count, visited_count
        visited_count += 1

        steps_visual.append(state[:])

        # Goal test
        if len(state) == n:
            if goal is None or state == goal:
                return state
            return None

        # Cutoff
        if depth == 0:
            return "cutoff"

        cutoff_occurred = False

        # Sinh các action (các cột chưa được chọn)
        for col in range(n):
            if col not in state:
                child = state + [col]
                expanded_count += 1  # mỗi child sinh ra → tăng expanded
                result = recursive_dls(child, depth - 1, frontier + [child])

                if result == "cutoff":
                    cutoff_occurred = True
                elif result is not None:
                    return result  # tìm thấy solution

        return "cutoff" if cutoff_occurred else None

    result = recursive_dls([], limit, [[]])

    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": 0,  # DLS dùng đệ quy, frontier không thể đếm chính xác => để 0 hoặc len(frontier cuối)
        "time": elapsed
    }
    return result, steps_visual, stats

def depth_limited_search_visual(n, goal=None, return_steps=False, return_stats=False, return_logs=False, limit=None):
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    if limit is None:
        limit = n

    steps = []
    logs = []
    visited_count = 0
    expanded_count = 0
    start_time = time.time()

    def recursive_dls(state, depth, frontier):
        nonlocal visited_count, expanded_count
        visited_count += 1
        steps.append(state[:])

        logs.append(f"Visiting: {state} | Depth left: {depth} | Stack: {frontier}")

        if len(state) == n:
            if goal is None or state == goal:
                logs.append(f"GOAL FOUND at state {state}")
                return state
            return None

        if depth == 0:
            return "cutoff"

        cutoff_occurred = False

        for col in range(n):
            if col not in state:
                child = state + [col]
                expanded_count += 1
                result = recursive_dls(child, depth - 1, frontier + [child])

                if result == "cutoff":
                    cutoff_occurred = True
                elif result is not None:
                    return result

        return "cutoff" if cutoff_occurred else None

    result = recursive_dls([], limit, [[]])

    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": 0,
        "time": elapsed
    }

    if return_stats and return_logs:
        return (result, steps, stats, logs)
    elif return_logs:
        return (result, steps, logs)
    elif return_stats:
        return (result, steps, stats)
    return (result, steps) if return_steps else result