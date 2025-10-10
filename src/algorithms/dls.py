import time

def depth_limited_search(n, goal=None, return_steps=False, return_stats=False, limit=None):
    """
    Depth-Limited Search (TREE-SEARCH version)
    - visited: số trạng thái đã được xét (được lấy ra để mở rộng)
    - expanded: tổng số trạng thái con đã được sinh ra
    - frontier: số trạng thái đang nằm trong stack (ước lượng theo lần gọi đệ quy)
    """
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    if limit is None:
        limit = n

    steps_visual = []   # dùng để animate
    steps_round  = []   # snapshot trạng thái "ngăn xếp"
    expanded_count = 0
    visited_count = 0

    start_time = time.time()

    def recursive_dls(state, depth, frontier):
        nonlocal expanded_count, visited_count
        visited_count += 1

        # Lưu snapshot (dùng cho visualize)
        steps_round.append(frontier[:])
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

    if return_stats:
        if return_steps:
            return result, steps_visual, stats
        return result, stats

    if return_steps:
        return result, steps_visual, steps_round

    return result

def depth_limited_search_visual(n, goal=None, return_steps=False, return_stats=False, return_logs=False, limit=None):
    """
    Depth-Limited Search (DLS) có visualization.
    - Hiển thị log từng bước và stack đệ quy.
    - return_logs: trả về log chi tiết để visualize từng bước.
    """
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    if limit is None:
        limit = n

    steps = []   # các state đã xét (cho visualization)
    logs = []    # mô tả từng bước
    visited_count = 0
    expanded_count = 0

    start_time = time.time()

    def recursive_dls(state, depth, frontier):
        nonlocal visited_count, expanded_count
        visited_count += 1
        steps.append(state[:])

        # Ghi log trạng thái hiện tại và ngăn xếp
        logs.append(f"Visiting: {state} | Depth left: {depth} | Stack: {frontier}")

        # Goal test
        if len(state) == n:
            if goal is None or state == goal:
                logs.append(f"GOAL FOUND at state {state}")
                return state
            return None

        # Cutoff (giới hạn độ sâu)
        if depth == 0:
            return "cutoff"

        cutoff_occurred = False

        # Sinh các action (cột chưa được chọn)
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
        "frontier": 0,  # DLS dùng đệ quy nên frontier không đếm chính xác
        "time": elapsed
    }

    if return_stats and return_logs:
        return (result, steps, stats, logs)
    elif return_logs:
        return (result, steps, logs)
    elif return_stats:
        return (result, steps, stats)
    return (result, steps) if return_steps else result