import random

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
            # Action: cố đặt vào cột col
            succ = []
            # Kết quả 1: thành công
            succ.append(state + [col])
            # Kết quả 2: bị đẩy (nếu còn cột khác)
            other_cols = [c for c in range(n) if c not in state and c != col]
            # if other_cols:
            #     pushed = random.choice(other_cols)
            #     succ.append(state + [pushed])
            for pushed in other_cols:
                succ.append(state + [pushed])
            results.append((col, succ))
    return results

def and_or_search(state, n, visited):
    """
    AND–OR search đệ quy cho hành động không xác định.
    Trả về:
      - Một plan dạng cây (dict) nếu thành công
      - None nếu thất bại
    """
    # Goal: đủ n quân
    if len(state) == n:
        return "GOAL"

    # Nếu đã thăm state này -> tránh lặp
    key = tuple(state)
    if key in visited:
        return None
    visited.add(key)

    # OR-node: ta phải chọn một hành động
    for action, outcomes in nondet_successors(state, n):
        # AND-node: mọi kết quả của hành động phải có kế hoạch tiếp
        subplans = []
        all_success = True
        for result_state in outcomes:
            subplan = and_or_search(result_state, n, visited)
            if subplan is None:
                all_success = False
                break
            subplans.append((result_state, subplan))
        if all_success:
            # Trả về plan cho hành động này
            return {"action": action, "results": subplans}

    return None


def extract_all_solutions(plan):
    """
    Duyệt toàn bộ cây kế hoạch và trả về danh sách
    TẤT CẢ các state đích (goal states) trong plan.
    """
    solutions = []

    def dfs(node):
        # Nếu đã tới goal, node chính là một state hoàn chỉnh
        if node == "GOAL":
            # Khi gặp "GOAL", state hiện tại đã được truyền vào từ cha
            return  # goal tự được xử lý ở cấp cha
        if isinstance(node, dict):
            for state, subplan in node["results"]:
                if subplan == "GOAL":
                    solutions.append(state)       # state hoàn chỉnh
                else:
                    dfs(subplan)                  # tiếp tục đi sâu

    dfs(plan)
    return solutions
