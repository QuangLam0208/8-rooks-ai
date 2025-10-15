from .dls import depth_limited_search, depth_limited_search_visual
import time

def iterative_deepening_search(n, goal=None):
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    total_expanded = 0
    total_visited = 0
    total_time = 0

    start_time = time.time()
    result = None

    for limit in range(n + 1):
        # chạy DLS với giới hạn độ sâu
        dls_result, dls_stats = depth_limited_search(n, goal, limit=limit)

        # Cộng dồn thống kê
        total_expanded += dls_stats["expanded"]
        total_visited += dls_stats["visited"]
        total_time += dls_stats["time"]

        # Nếu DLS tìm thấy lời giải thật sự thì dừng luôn
        if dls_result not in (None, "cutoff"):
            result = dls_result
            break

    elapsed = (time.time() - start_time) * 1000
    final_stats = {
        "expanded": total_expanded,
        "visited": total_visited,
        "frontier": 0,
        "time": elapsed
    }
    return result, final_stats

def iterative_deepening_search_visual(n, goal=None, return_steps=False, return_stats=False, return_logs=False):
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    steps = []
    logs = []
    total_expanded = 0
    total_visited = 0
    result = None

    start_time = time.time()

    for limit in range(n + 1):
        dls_result, dls_steps, dls_stats, dls_logs = depth_limited_search_visual(
            n, goal, return_steps=True, return_stats=True, return_logs=True, limit=limit
        )

        steps.extend([s for s in dls_steps if isinstance(s, list)])
        logs.extend(dls_logs)

        total_expanded += dls_stats["expanded"]
        total_visited += dls_stats["visited"]

        if dls_result not in (None, "cutoff"):
            result = dls_result
            break

    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": total_expanded,
        "visited": total_visited,
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