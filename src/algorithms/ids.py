from .dls import depth_limited_search

def iterative_deepening_search(n, goal=None):
    """
    Iterative Deepening Search (IDS)
    - n: kích thước bàn cờ (số hàng/cột)
    - goal: list các cột (vd: [0,1,3,2]) hoặc None (tìm solution bất kỳ)
    
    Thực hiện gọi DLS với limit = 0,1,...,n
    Trả về solution (list cột) hoặc None nếu không tìm thấy.
    """
    if goal is not None and isinstance(goal, tuple):
        goal = list(goal)

    for limit in range(n + 1):
        result = depth_limited_search(n, goal, limit)
        if result is not None:
            return result
    return None
