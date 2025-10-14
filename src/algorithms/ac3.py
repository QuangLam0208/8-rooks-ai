import time
from collections import deque

def ac3_search(n, goal=None, return_steps=False, return_stats=False, max_expansions=None):
    """
    Backtracking + AC-3 cho bài toán đặt n quân xe.
    Giữ nguyên toàn bộ logic gốc.
    Thêm thống kê: expanded, visited, frontier, time.
    Thêm giới hạn max_expansions để tránh chạy vô hạn (nếu muốn).
    """

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

    # Ràng buộc: 2 quân xe không được cùng cột
    def constraint(xi, vi, xj, vj):
        return vi != vj

    # --- Thuật toán AC-3 ---
    def ac3(domains):
        queue = deque([(xi, xj) for xi in range(n) for xj in range(n) if xi != xj])
        while queue:
            xi, xj = queue.popleft()
            if revise(domains, xi, xj):
                if not domains[xi]:
                    return False
                for xk in range(n):
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(domains, xi, xj):
        revised = False
        to_remove = []
        for vi in domains[xi]:
            if not any(constraint(xi, vi, xj, vj) for vj in domains[xj]):
                to_remove.append(vi)
        if to_remove:
            for vi in to_remove:
                domains[xi].remove(vi)
            revised = True
        return revised

    # --- Backtracking + AC-3 ---
    def backtrack(state, domains):
        nonlocal expanded, visited
        visited += 1

        # Nếu đủ n quân -> kiểm tra goal
        if len(state) == n:
            if goal_list is not None:
                return state if state == goal_list else None
            return state

        row = len(state)
        for col in list(domains[row]):  # duyệt giá trị trong miền hiện tại
            if col not in state:
                expanded += 1
                if max_expansions is not None and expanded > max_expansions:
                    return None

                new_domains = [d[:] for d in domains]
                new_domains[row] = [col]  # gán hàng row = col

                # Duy trì consistency với AC-3
                if ac3(new_domains):
                    result = backtrack(state + [col], new_domains)
                    if result is not None:
                        return result

        return None

    # --- Chạy ---
    domains = [list(range(n)) for _ in range(n)]
    res = backtrack([], domains)

    elapsed = (time.time() - start_time) * 1000  # ms
    stats = {
        "expanded": expanded,
        "visited": visited,
        "frontier": 0,  # frontier không áp dụng trong backtracking
        "time": elapsed
    }

    # --- Trả kết quả ---
    if return_stats:
        if return_steps:
            return res, stats
        return res, stats
    if return_steps:
        return res
    return res
