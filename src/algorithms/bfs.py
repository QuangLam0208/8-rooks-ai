from collections import deque

def breadth_first_search(n, goal=None, return_steps=False):
    """
    BFS đặt n quân xe.
    - Nếu return_steps = False: trả về state cuối cùng (như cũ).
    - Nếu return_steps = True: trả về (goal_state, steps)
    """
    queue = deque([[]])  
    steps = []  

    while queue:
        state = queue.popleft()
        steps.append(state)

        row = len(state)
        if row == n:
            if goal is not None and isinstance(goal, tuple):
                goal = list(goal)
            if state == goal:
                return (state, steps) if return_steps else state
            continue  # nếu khác goal thì bỏ qua

        # mở rộng
        for col in range(n):
            if col not in state:
                queue.append(state + [col])

    return (None, steps) if return_steps else None