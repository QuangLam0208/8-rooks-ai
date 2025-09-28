def depth_limited_search(n, goal=None, return_steps=False, limit=None):
    """
    Depth-Limited Search (TREE-SEARCH version)
    - n: kích thước bàn cờ (số hàng/cột)
    - goal: list các cột (ví dụ [0,1,3,2]) hoặc None (chỉ cần tìm một solution bất kỳ)
    - limit: độ sâu tối đa, thường = n
    Trả về solution (list cột) hoặc None nếu không tìm thấy.
    """
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    if limit is None:
        limit = n

    steps_visual = []   # các state đã được expand (dùng để animate)
    steps_round  = []   # snapshot trạng thái "ngăn xếp" sau mỗi lần pop (dùng để in console)

    def recursive_dls(state, depth, frontier):
        """
        state: đường đi hiện tại
        depth: độ sâu còn lại
        frontier: danh sách mô phỏng stack hiện tại (chỉ để lưu console)
        """
        # Lưu snapshot để in console
        steps_round.append(frontier[:])
        # Lưu state vừa pop ra để visualize
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

        # Sinh action (các cột chưa được chọn)
        for col in range(n):
            if col not in state:
                child = state + [col]
                result = recursive_dls(child, depth - 1, frontier + [child])

                if result == "cutoff":
                    cutoff_occurred = True
                elif result is not None:
                    return result  # tìm thấy solution

        return "cutoff" if cutoff_occurred else None

    result = recursive_dls([], limit, [[]])

    if return_steps:
        if result == "cutoff" or result is None:
            return None, steps_visual, steps_round
        return result, steps_visual, steps_round

    if result == "cutoff" or result is None:
        return None
    return result
