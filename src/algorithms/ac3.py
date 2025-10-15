import time
from collections import deque

def ac3_search(n, goal=None, max_expansions=None):
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

    domains = [list(range(n)) for _ in range(n)]
    res = backtrack([], domains)

    elapsed = (time.time() - start_time) * 1000  # ms
    stats = {
        "expanded": expanded,
        "visited": visited,
        "frontier": 0,  # frontier không áp dụng trong backtracking
        "time": elapsed
    }
    return res, stats

def ac3_search_visual(n, goal=None, return_steps=False, return_logs=False, max_expansions=None):
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
    steps_visual = []
    logs = []
    found_result = None

    def add_step(state, message, depth=0):
        indent = "   " * depth
        logs.append(f"{indent}{message}")
        steps_visual.append(state[:])

    def constraint(xi, vi, xj, vj):
        return vi != vj

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

    def ac3(domains, depth=0, state=None):
        queue = deque([(xi, xj) for xi in range(n) for xj in range(n) if xi != xj])
        add_step(state or [], f"{'   '*depth}Run AC-3: start with {len(queue)} arcs.", depth)
        while queue:
            xi, xj = queue.popleft()
            if revise(domains, xi, xj):
                add_step(state or [], f"{'   '*depth}Revise({xi},{xj}) → domains[{xi}]={domains[xi]}", depth)
                if not domains[xi]:
                    add_step(state or [], f"{'   '*depth}  Domain of X{xi} empty → fail", depth)
                    return False
                for xk in range(n):
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))
        add_step(state or [], f"{'   '*depth}AC-3 consistent.", depth)
        return True

    def backtrack(state, domains, depth=0):
        nonlocal expanded, visited, found_result
        visited += 1

        add_step(state, f"Visit state: {state}", depth)

        # Nếu đủ n quân -> kiểm tra goal
        if len(state) == n:
            if goal_list is not None:
                if state == goal_list:
                    found_result = state
                    add_step(state, f"Found GOAL: {state}", depth)
                    return state
                else:
                    add_step(state, f"Reached leaf {state}, not goal.", depth)
                    return None
            else:
                found_result = state
                add_step(state, f"Found valid full state: {state}", depth)
                return state

        row = len(state)
        for col in list(domains[row]):
            if col not in state:
                expanded += 1
                add_step(state, f"  Try assigning row {row} = col {col}", depth)

                if max_expansions is not None and expanded > max_expansions:
                    add_step(state, f"  Expansion limit reached ({max_expansions}), stop.", depth)
                    return None

                new_domains = [d[:] for d in domains]
                new_domains[row] = [col]  # gán hàng hiện tại

                # Duy trì tính nhất quán với AC-3
                if ac3(new_domains, depth + 1, state + [col]):
                    result = backtrack(state + [col], new_domains, depth + 1)
                    if result is not None:
                        return result
                else:
                    add_step(state, f"  AC-3 inconsistency after assigning row {row}={col}", depth)

                add_step(state, f"  Backtrack from {state + [col]}", depth)

        add_step(state, f"No valid move from {state}, return None", depth)
        return None

    # ====== Bắt đầu ======
    domains = [list(range(n)) for _ in range(n)]
    result = backtrack([], domains)

    elapsed = (time.time() - start_time) * 1000  # ms
    stats = {
        "expanded": expanded,
        "visited": visited,
        "frontier": 0,
        "time": elapsed
    }

    if result is None:
        add_step([], "  No solution found.")
    else:
        add_step(result, f"  Finished. Result: {result}")

    if return_steps and return_logs:
        return result, steps_visual, logs
    elif return_steps:
        return result, steps_visual
    elif return_logs:
        return result, logs
    else:
        return result