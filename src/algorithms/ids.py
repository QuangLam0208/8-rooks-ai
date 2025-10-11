from .dls import depth_limited_search, depth_limited_search_visual
import time

def iterative_deepening_search(n, goal=None):
    """
    Iterative Deepening Search (IDS)
    - Gọi DLS với limit tăng dần từ 0 đến n
    - Cộng dồn số liệu từ các lần chạy DLS
    - Trả về (result, steps, stats) nếu return_stats=True
    """
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    steps_visual_all = []  # toàn bộ các state expand được

    total_expanded = 0
    total_visited = 0
    total_time = 0

    start_time = time.time()
    result = None

    for limit in range(n + 1):
        # chạy DLS với giới hạn độ sâu
        dls_result, dls_steps, dls_stats = depth_limited_search(
            n, goal, return_steps=True, return_stats=True, limit=limit
        )

        steps_visual_all.extend(dls_steps)

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
    return result, steps_visual_all, final_stats

def iterative_deepening_search_visual(n, goal=None, return_steps=False, return_stats=False, return_logs=False):
    """
    Iterative Deepening Search (IDS) có visualization.
    - Gọi depth_limited_search_visual với limit tăng dần từ 0 đến n.
    - Gộp toàn bộ steps và logs lại.
    """
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

        # Chỉ thêm các state thực sự được xét (không thêm snapshot stack)
        steps.extend([s for s in dls_steps if isinstance(s, list)])
        logs.extend(dls_logs)

        # Cộng thống kê
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

    # --- Trả về theo các chế độ ---
    if return_stats and return_logs:
        return (result, steps, stats, logs)
    elif return_logs:
        return (result, steps, logs)
    elif return_stats:
        return (result, steps, stats)
    return (result, steps) if return_steps else result