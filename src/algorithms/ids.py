from .dls import depth_limited_search

def iterative_deepening_search(n, goal=None, return_steps=False):
    """
    Iterative Deepening Search (IDS)
    - n: kích thước bàn cờ (số hàng/cột)
    - goal: list các cột (vd: [0,1,3,2]) hoặc None (tìm solution bất kỳ)
    
    Thực hiện gọi DLS với limit = 0,1,...,n
    Trả về solution (list cột) hoặc None nếu không tìm thấy.
    """
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    # Lưu tất cả các bước cho visualize/console
    steps_visual_all = []  # toàn bộ các state được expand (theo thứ tự IDS)
    steps_round_all  = []  # snapshot từng lần DLS

    for limit in range(n + 1):
        if return_steps:
            result, vis, round_steps = depth_limited_search(n, goal, True, limit)
            # Chèn marker để phân biệt vòng limit
            steps_round_all.append([f"--- LIMIT {limit} ---"])
            steps_round_all.extend(round_steps)
            steps_visual_all.extend(vis)
        else:
            result = depth_limited_search(n, goal, limit)

        if result is not None:
            if return_steps:
                return result, steps_visual_all, steps_round_all
            return result

    if return_steps:
        return None, steps_visual_all, steps_round_all
    return None
