def backtracking_search(n, goal=None, return_steps=False):
    """
    Backtracking cơ bản cho bài toán đặt n quân xe.
    - Nếu return_steps = False: trả về state cuối cùng (nếu tìm thấy).
    - Nếu return_steps = True: trả về (goal_state, steps).
    """
    # Normalize goal -> list or None
    if goal is not None:
        try:
            goal_list = list(goal)
        except TypeError:
            goal_list = None
    else:
        goal_list = None

    steps = []

    def backtrack(state):
        steps.append(state[:])

        # kiểm tra goal / solution
        if len(state) == n:
            if goal_list is not None:
                if state == goal_list:
                    return state
                else:
                    return None
            else:
                return state

        # thử đặt quân xe ở cột hợp lệ (miền = 0..n-1)
        for col in range(n):
            if col not in state:  # ràng buộc: không trùng cột
                result = backtrack(state + [col])
                if result is not None:
                    return result

        return None

    res = backtrack([])
    return (res, steps) if return_steps else res
