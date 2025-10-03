def forward_checking_search(n, goal=None, return_steps=False):
    # Normalize goal
    if goal is not None:
        try:
            goal_list = list(goal)
        except TypeError:
            goal_list = None
    else:
        goal_list = None

    steps = []

    def forward_check(state, domains):
        steps.append(state[:])

        if len(state) == n:
            if goal_list is not None:
                if state == goal_list:
                    return state
                else:
                    return None
            else:
                return state

        row = len(state)
        for col in list(domains[row]):   # iterate on a snapshot
            if col not in state:
                # cập nhật miền giá trị cho các hàng tiếp theo
                new_domains = [d[:] for d in domains]
                for r in range(row + 1, n):
                    if col in new_domains[r]:
                        new_domains[r].remove(col)

                # nếu không hàng nào bị mất hết miền giá trị thì tiếp tục
                if all(len(d) > 0 for r, d in enumerate(new_domains) if r > row):
                    result = forward_check(state + [col], new_domains)
                    if result is not None:
                        return result

        return None

    domains = [list(range(n)) for _ in range(n)]
    res = forward_check([], domains)
    return (res, steps) if return_steps else res
