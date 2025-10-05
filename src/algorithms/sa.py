import math, random, time
from .heuristic import h_partial

def expand_partial(state, n):
    successors = []
    row = len(state)
    if row < n:
        for col in range(n):
            if col not in state:
                successors.append(state + [col])
    return successors


def simulated_annealing(n, goal, return_steps=False, return_stats=False,
                        heuristic=h_partial, max_iter=10000):
    """
    Simulated Annealing đặt từng quân.
    - expanded: số successor sinh ra
    - visited: số bước đã xét (mỗi lần lặp)
    - frontier: 0 (vì không lưu tập chờ)
    """
    start_time = time.time()
    goal = list(goal) if isinstance(goal, tuple) else goal

    current = []  # bắt đầu rỗng
    best = current[:]
    best_score = heuristic(current, goal)

    steps_visual = []
    steps_console = []

    expanded_count = 0
    visited_count = 0

    t = 1
    for _ in range(max_iter):
        T = max(0.01, 1000 / (t + 1))
        visited_count += 1

        if return_steps:
            h_curr = heuristic(current, goal)
            steps_visual.append(current[:])
            steps_console.append((t, round(T, 3), current[:], h_curr))

        if current == goal:
            break

        successors = expand_partial(current, n)
        expanded_count += len(successors)
        if not successors:
            break

        scored = [(heuristic(s, goal), s) for s in successors]
        scored.sort(key=lambda x: x[0])
        best_s_h, best_s = scored[0]

        curr_h = heuristic(current, goal)
        if best_s_h < curr_h:
            current = best_s
        else:
            next_state = random.choice(successors)
            deltaE = curr_h - heuristic(next_state, goal)
            if deltaE > 0:
                current = next_state
            else:
                if random.random() < math.exp(deltaE / T):
                    current = next_state

        # cập nhật best nếu tốt hơn
        score = heuristic(current, goal)
        if score < best_score:
            best = current[:]
            best_score = score

        t += 1

    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded_count,
        "visited": visited_count,
        "frontier": 0,
        "time": elapsed
    }

    # trả kết quả
    result = best if best_score == 0 else None
    if return_stats:
        if return_steps:
            return result, steps_visual, stats
        return result, stats
    if return_steps:
        return result, steps_visual, steps_console
    return result
