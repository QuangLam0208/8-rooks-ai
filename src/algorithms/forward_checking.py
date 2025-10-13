import time

def forward_checking_search(n, goal=None, return_steps=False, return_stats=False, max_expansions=None):
    """
    Forward Checking cho bài toán đặt n quân xe.
    Thêm thống kê expanded, visited, frontier, time
    Thêm bảo vệ tránh đệ quy vô hạn bằng max_expansions
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
    steps = [] if return_steps else None
    expanded = 0
    visited = 0

    def forward_check(state, domains):
        nonlocal expanded, visited
        visited += 1
        if return_steps:
            steps.append(state[:])

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

    # Trả kết quả phù hợp mode gọi
    if return_stats:
        if return_steps:
            return res, steps, stats
        return res, stats
    if return_steps:
        return res, steps
    return res
