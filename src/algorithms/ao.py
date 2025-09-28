from collections import deque

def and_or_bfs(n, goal=None, return_steps=False):
    """
    AND-OR Search sử dụng BFS để đặt n quân xe.
    - n: số quân xe (8 trong bài toán 8 rooks)
    - goal: state đích (list hoặc tuple), hoặc None để chấp nhận mọi state đầy đủ
    - return_steps=False:
         + False -> chỉ trả về state tìm thấy (Run)
         + True  -> trả về (state, steps) để Visualization
    """
    # hàng đợi BFS, mỗi phần tử = state hiện tại (list các cột đã chọn)
    queue = deque([[]])
    steps = []  # lưu tất cả các state đã duyệt (dùng cho visualization)

    while queue:
        state = queue.popleft()
        steps.append(state)  # ghi nhận bước đã duyệt

        # Nếu đã đặt đủ n quân
        if len(state) == n:
            # Chuẩn hóa goal (nếu có)
            if goal is not None and isinstance(goal, tuple):
                goal = list(goal)
            # Kiểm tra goal
            if goal is None or state == goal:
                return (state, steps) if return_steps else state
            # Không phải goal thì bỏ qua (không mở rộng nữa)
            continue

        # ---------- AND phần ----------
        # Với AND, ta yêu cầu tất cả các hành động khả thi đều được kiểm tra
        actions = []
        for col in range(n):
            # điều kiện hợp lệ: không trùng cột (vì mỗi hàng 1 xe)
            if col not in state:
                actions.append(col)

        # Nếu không có hành động nào => fail (AND thất bại)
        if not actions:
            # Không mở rộng gì, BFS sẽ tự bỏ state này
            continue

        # ---------- OR phần ----------
        # Duyệt tất cả action (OR: chỉ cần 1 nhánh thành công)
        # BFS nghĩa là chỉ cần enqueue các nhánh hợp lệ, 
        # và vòng lặp sẽ tiếp tục xử lý từng nhánh
        for col in actions:
            new_state = state + [col]
            queue.append(new_state)

    # Nếu duyệt hết vẫn không tìm thấy goal
    return (None, steps) if return_steps else None
