from collections import deque

def ac3_search(n, goal=None, return_steps=False):
    """
    Backtracking + AC-3 cho bài toán đặt n quân xe.
    - Nếu return_steps = True: trả về (solution, steps).
    - Nếu return_steps = False: chỉ trả về solution.
    """

    # Normalize goal
    if goal is not None:
        try:
            goal_list = list(goal)
        except TypeError:
            goal_list = None
    else:
        goal_list = None

    steps = []

    # Hàm kiểm tra ràng buộc binary: Xi != Xj (khác cột)
    def constraint(xi, vi, xj, vj):
        return vi != vj

    # Thuật toán AC-3
    def ac3(domains):
        queue = deque([(xi, xj) for xi in range(n) for xj in range(n) if xi != xj])
        while queue:
            xi, xj = queue.popleft()
            if revise(domains, xi, xj):
                if not domains[xi]:  # nếu mất hết miền giá trị
                    return False
                for xk in range(n):
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(domains, xi, xj):
        revised = False
        to_remove = []
        for vi in domains[xi]:
            # nếu không tồn tại giá trị vj nào thỏa ràng buộc thì loại vi
            if not any(constraint(xi, vi, xj, vj) for vj in domains[xj]):
                to_remove.append(vi)
        if to_remove:
            for vi in to_remove:
                domains[xi].remove(vi)
            revised = True
        return revised

    # Backtracking với AC-3
    def backtrack(state, domains):
        steps.append(state[:])

        if len(state) == n:
            if goal_list is not None:
                return state if state == goal_list else None
            else:
                return state

        row = len(state)
        for col in list(domains[row]):  # thử từng giá trị trong miền
            if col not in state:
                new_domains = [d[:] for d in domains]
                new_domains[row] = [col]  # gán row = col

                if ac3(new_domains):  # chạy AC-3 để duy trì consistency
                    result = backtrack(state + [col], new_domains)
                    if result is not None:
                        return result

        return None

    domains = [list(range(n)) for _ in range(n)]
    res = backtrack([], domains)
    return (res, steps) if return_steps else res
