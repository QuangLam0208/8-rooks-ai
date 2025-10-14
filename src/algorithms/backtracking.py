import time

def backtracking_search(n, goal=None, max_expansions=None):
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

    found_result = None

    def backtrack(state):
        nonlocal expanded, visited, found_result
        visited += 1

        # nếu đạt goal
        if len(state) == n:
            if goal_list is not None:
                if state == goal_list:
                    found_result = state
                    return state
                return None
            else:
                found_result = state
                return state

        # sinh tiếp các nhánh hợp lệ
        for col in range(n):
            if col not in state:
                expanded += 1
                if max_expansions is not None and expanded > max_expansions:
                    return None
                result = backtrack(state + [col])
                if result is not None:
                    return result

        return None

    res = backtrack([])

    elapsed = (time.time() - start_time) * 1000  # ms
    stats = {
        "expanded": expanded,
        "visited": visited,
        "frontier": 0,   # frontier không có ý nghĩa rõ ràng trong backtracking (stack đệ quy)
        "time": elapsed
    }
    return res, stats
