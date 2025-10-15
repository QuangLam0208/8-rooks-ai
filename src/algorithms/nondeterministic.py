import time

# def nondet_successors(state, n):
#     """
#     Sinh các kết quả có thể xảy ra khi thực hiện hành động PlaceRook.
#     Giới hạn: Mỗi hành động chỉ sinh TỐI ĐA 2 kết quả (OK và FAIL).
#     """
#     import random
#     row = len(state)
#     results = []
#     available_cols = [c for c in range(n) if c not in state]

#     for col in available_cols:
#         outcomes = []

#         # Kết quả 1: thành công (đặt đúng cột mong muốn)
#         outcomes.append(state + [col])

#         # Kết quả 2: thất bại (đặt nhầm sang 1 cột khác ngẫu nhiên)
#         other_cols = [c for c in available_cols if c != col]
#         if other_cols:
#             fail_col = random.choice(other_cols)
#             outcomes.append(state + [fail_col])

#         results.append((col, outcomes))

#     return results

def nondet_successors(state, n):
    """
    Sinh tất cả các kết quả có thể xảy ra khi thực hiện hành động PlaceRook.
    - Mỗi action (đặt quân vào 1 cột) tạo ra tất cả cột khả thi chưa được dùng.
    """
    row = len(state)
    results = []
    available_cols = [c for c in range(n) if c not in state]

    for col in available_cols:
        outcomes = []
        # Sinh tất cả cột khả thi
        for out_col in available_cols:
            outcomes.append(state + [out_col])
        results.append((col, outcomes))

    return results

def and_or_search(n, goal=None):
    '''
    Or node: là các action 0, 1, ... (hành động đặt cột 0, 1...)\
    And node: là những kết quả của action (đặt đúng cột đã chọn, đặt sai cột)
    Chỉ cần 1 Or node (action) đúng (có plan) -> cây đúng (có plan)
    Phải tất cả các And node (kết quả của action) đúng thì Or node mới đúng. 
    '''
    start_time = time.time()
    visited = []
    expanded = 0

    def recursive_search(state, path):
        nonlocal expanded
        visited.append(state[:])

        # Goal reached
        if len(state) == n:
            return ["GOAL"]

        key = tuple(state)
        if key in path:
            return []  # tránh vòng lặp

        path.add(key)
        succs = nondet_successors(state, n)

        # OR-node: chỉ cần 1 hành động có kế hoạch hợp lệ
        for action, outcomes in succs:
            expanded += len(outcomes)
            outcome_subplans = []
            failure = False

            # AND-node: mọi outcome đều phải có kế hoạch
            for outcome_state in outcomes:
                subplans = recursive_search(outcome_state, path)
                if not subplans:  # 1 outcome thất bại → cả action fail
                    failure = True
                    break
                outcome_subplans.append((outcome_state, subplans[0]))  # lấy 1 plan thôi

            if not failure:
                # Hành động này thành công → dừng, trả về kế hoạch đầu tiên
                plan = {"action": action, "results": outcome_subplans}
                path.remove(key)
                return [plan]

        # Không có action nào thành công → node này thất bại
        path.remove(key)
        return []

    # bắt đầu từ root
    plans = recursive_search([], set())

    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded,
        "visited": len(visited),
        "frontier": 0,
        "time": elapsed
    }

    # In cây kế hoạch (nếu có)
    if plans:
        # for i, plan in enumerate(plans):
        #     print(f"\n===== CÂY KẾ HOẠCH #{i+1} =====")
        #     print_and_or_tree(plan)
        all_states = extract_all_solutions(plans)
        if goal and goal in all_states:
            result = goal
        else:
            result = all_states[0] if all_states else None 
    else:
        print("\nKhông có kế hoạch khả thi nào.")
        result = None

    return result, stats

def and_or_search_visual(n, goal=None, return_steps=False, return_logs=False):
    start_time = time.time()
    steps_visual = []
    expanded = 0

    def recursive_search(state, path):
        nonlocal expanded
        steps_visual.append(state[:])
        if state != []:
            steps_visual.append(state[:])

        # Goal reached
        if len(state) == n:
            return ["GOAL"]

        key = tuple(state)
        if key in path:
            return []  # tránh vòng lặp

        path.add(key)
        succs = nondet_successors(state, n)

        # OR-node: chỉ cần 1 hành động có kế hoạch hợp lệ
        for action, outcomes in succs:
            expanded += len(outcomes)
            outcome_subplans = []
            failure = False

            # AND-node: mọi outcome đều phải có kế hoạch
            for outcome_state in outcomes:
                subplans = recursive_search(outcome_state, path)
                if not subplans:  # 1 outcome thất bại → cả action fail
                    failure = True
                    break
                outcome_subplans.append((outcome_state, subplans[0]))  # lấy 1 plan thôi

            if not failure:
                # Hành động này thành công → dừng, trả về kế hoạch đầu tiên
                plan = {"action": action, "results": outcome_subplans}
                path.remove(key)
                return [plan]

        # Không có action nào thành công → node này thất bại
        path.remove(key)
        return []

    # bắt đầu từ root
    plans = recursive_search([], set())

    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded,
        "visited": len(steps_visual),
        "frontier": 0,
        "time": elapsed
    }

    # In cây kế hoạch (nếu có)
    plan_logs = []
    if plans:
        for i, plan in enumerate(plans):
            print(f"\n===== CÂY KẾ HOẠCH #{i+1} =====")
            print_and_or_tree(plan)
            plan_logs.extend(tree_to_strings(plan))
        all_states = extract_all_solutions(plans)
        if goal and goal in all_states:
            result = goal
        else:
            result = all_states[0] if all_states else None 
    else:
        plan_logs.append("Không có kế hoạch khả thi nào.")
        result = None

    if return_logs:
        if return_steps:
            return result, steps_visual, plan_logs

def tree_to_strings(plan, indent="", label="ROOT"):
    """
    Chuyển cây AND-OR thành danh sách các string để hiển thị trên bảng trắng
    """
    lines = []

    if plan == "GOAL":
        lines.append(f"{indent}({label}) → GOAL")
        return lines

    if isinstance(plan, list):
        for subplan in plan:
            lines.extend(tree_to_strings(subplan, indent, label))
        return lines

    action = plan.get("action", "?")
    lines.append(f"{indent}{label} ── action {action}")

    for idx, (state, subplan) in enumerate(plan["results"]):
        outcome_label = "OK" if idx == 0 else "FAIL"
        lines.append(f"{indent}   ├── {outcome_label}: {state}")
        lines.extend(tree_to_strings(subplan, indent + "   │   ", label=""))

    return lines

def print_and_or_tree(plan, indent="", label="ROOT"):
    """
    In ra toàn bộ cây kế hoạch AND–OR (với nhánh action + outcome).
    - plan: cây kế hoạch dạng dict hoặc "GOAL"
    - indent: chuỗi thụt lề để hiển thị đẹp
    - label: nhãn hiện tại (ví dụ "OK", "FAIL", hoặc "ROOT")
    """
    # Nếu plan là "GOAL" thì in kết thúc
    if plan == "GOAL":
        print(f"{indent}({label}) → GOAL")
        return

    # Nếu plan là list (nhiều plan) thì duyệt từng cái
    if isinstance(plan, list):
        for subplan in plan:
            print_and_or_tree(subplan, indent, label)
        return

    # Nếu plan là dict, hiển thị action + các kết quả
    action = plan.get("action", "?")
    print(f"{indent}{label} ── action {action}")

    # Duyệt các kết quả của action (AND-node)
    for (state, subplan) in plan["results"]:
        # Gán nhãn cho mỗi outcome
        outcome_label = "OK" if plan["results"].index((state, subplan)) == 0 else "FAIL"
        outcome_label = f"{outcome_label}: {state}"
        print(f"{indent}   ├── {outcome_label}")
        print_and_or_tree(subplan, indent + "   │   ", label="")

def extract_all_solutions(plans):
    """
    Nhận một danh sách plans (kết quả của and_or_search_all) và trả về
    danh sách tất cả các trạng thái đích (state) xuất hiện như outcomes dẫn tới "GOAL".
    """
    solutions = []

    def dfs_node(node):
        # node có thể là "GOAL" hoặc dict {"action":..., "results":[(state, subplan), ...]}
        if node == "GOAL":
            return True  # đỉnh là goal
        if isinstance(node, dict):
            found_any = False
            for state, subplan in node["results"]:
                if subplan == "GOAL":
                    solutions.append(state)
                    found_any = True
                else:
                    # subplan có thể là "GOAL" hoặc 1 dict, hoặc list (trường hợp khi kế hoạch lồng nhiều plan)
                    # để tương thích: nếu subplan là list (nhiều kế hoạch), duyệt tất cả
                    if isinstance(subplan, list):
                        for sp in subplan:
                            if sp == "GOAL":
                                solutions.append(state)
                                found_any = True
                            else:
                                if dfs_node(sp):
                                    found_any = True
                    else:
                        if dfs_node(subplan):
                            found_any = True
            return found_any
        return False

    # plans là danh sách các plan root; mỗi phần tử có thể là "GOAL" hoặc dict
    for p in plans:
        if p == "GOAL":
            # trường hợp plan trả về trực tiếp GOAL (khi start state là goal)
            solutions.append([])  # start state rỗng mà là goal (n=0) — hiếm khi xảy ra
        else:
            dfs_node(p)

    # loại trùng nếu cần
    unique_solutions = []
    seen = set()
    for s in solutions:
        t = tuple(s)
        if t not in seen:
            seen.add(t)
            unique_solutions.append(s)
    return unique_solutions