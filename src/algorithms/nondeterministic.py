import random, time

def nondet_successors(state, n):
    """
    Sinh các kết quả có thể xảy ra khi thực hiện hành động PlaceRook
    - state: danh sách cột đã chọn, độ dài = số hàng đã đặt.
    - n: kích thước bàn cờ (8 cho 8 rooks).
    """
    row = len(state)
    results = []
    for col in range(n):
        if col not in state:  # cột hợp lệ
            succ = []
            # Kết quả 1: thành công
            succ.append(state + [col])
            # Kết quả 2: thất bại (đặt trúng vị trí khác)
            other_cols = [c for c in range(n) if c not in state and c != col]
            for pushed in other_cols:
                succ.append(state + [pushed])
            results.append((col, succ))
    return results


def and_or_search(n, goal=None, return_steps=False, return_stats=False):
    """
    AND-OR search cho môi trường không xác định.
    - n: kích thước bàn cờ (8)
    - goal: trạng thái đích (list)
    - return_steps: lưu các state để visualize
    - return_stats: trả về thống kê (expanded, visited, frontier, time)
    """

    start_time = time.time()
    visited = set()
    expanded = 0

    steps_visual = []  # để animate
    steps_console = []  # để in console

    def recursive_search(state):
        nonlocal expanded

        # Lưu lại state đang xét
        if return_steps:
            steps_visual.append(state[:])
            steps_console.append(("Expand", state[:]))

        # Goal
        if len(state) == n:
            return "GOAL"

        key = tuple(state)
        if key in visited:
            return None
        visited.add(key)

        # OR-node: thử từng hành động (đặt vào từng cột)
        for action, outcomes in nondet_successors(state, n):
            expanded += 1
            subplans = []
            all_success = True

            # AND-node: mọi kết quả của hành động đều phải thành công
            for result_state in outcomes:
                subplan = recursive_search(result_state)
                if subplan is None:
                    all_success = False
                    break
                subplans.append((result_state, subplan))

            if all_success:
                return {"action": action, "results": subplans}

        return None

    # Bắt đầu tìm kiếm từ state rỗng
    plan = recursive_search([])

    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded,
        "visited": len(visited),
        "frontier": 0,
        "time": elapsed
    }

    # Trích xuất toàn bộ goal states (nếu có)
    if plan:
        all_states = extract_all_solutions(plan)
        if goal and goal in all_states:
            result = goal
        else:
            result = all_states[0] if all_states else None
    else:
        result = None

    # Trả kết quả đúng format
    if return_stats:
        if return_steps:
            return result, steps_visual, stats
        return result, stats
    if return_steps:
        return result, steps_visual, steps_console
    return result


def extract_all_solutions(plan):
    """Duyệt toàn bộ cây kế hoạch để lấy danh sách các state đích."""
    solutions = []

    def dfs(node):
        if node == "GOAL":
            return
        if isinstance(node, dict):
            for state, subplan in node["results"]:
                if subplan == "GOAL":
                    solutions.append(state)
                else:
                    dfs(subplan)

    dfs(plan)
    return solutions
