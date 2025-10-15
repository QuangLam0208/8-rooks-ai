import random, time
from .heuristic import h_misplaced, h_partial

def fitness(state, goal, heuristic):
    return -heuristic(state, goal)

def tournament_selection(pop, goal, heuristic, k=3):
    return max(random.sample(pop, k), key=lambda s: fitness(s, goal, heuristic))

def order_crossover(p1, p2):
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[a:b] = p1[a:b]
    hole = set(p1[a:b])
    fill = [x for x in p2 if x not in hole]
    j = 0
    for i in range(n):
        if child[i] is None:
            child[i] = fill[j]; j += 1
    return child

def mutate(state, rate=0.1):
    s = state[:]
    if random.random() < rate:
        i, j = random.sample(range(len(s)), 2)
        s[i], s[j] = s[j], s[i]
    return s

def genetic_algorithm(n, goal, heuristic=h_misplaced,
    pop_size=50, generations=500, crossover_rate=0.9,mutation_rate=0.1
):
    start_time = time.time()
    population = [random.sample(range(n), n) for _ in range(pop_size)]

    expanded = len(population)
    visited = 0

    result = None

    for g in range(1, generations + 1):
        best_curr = min(population, key=lambda s: heuristic(s, goal))
        h_best = heuristic(best_curr, goal)

        # Duyệt toàn bộ quần thể hiện tại
        for s in population:
            visited += 1
            if s == goal:
                result = s
                break

        if result is not None:
            break  # dừng vòng ngoài

        # Sinh thế hệ mới
        new_pop = []
        while len(new_pop) < pop_size:
            p1 = tournament_selection(population, goal, heuristic)
            p2 = tournament_selection(population, goal, heuristic)

            if random.random() < crossover_rate:
                c1 = order_crossover(p1, p2)
                c2 = order_crossover(p2, p1)
            else:
                c1, c2 = p1[:], p2[:]

            c1 = mutate(c1, mutation_rate)
            c2 = mutate(c2, mutation_rate)
            new_pop.extend([c1, c2])
            expanded += 2

        population = new_pop

    # Tính thống kê cuối
    elapsed = (time.time() - start_time) * 1000
    best = result if result else min(population, key=lambda s: heuristic(s, goal))

    stats = {
        "expanded": expanded,
        "visited": visited,
        "frontier": 0,
        "time": elapsed
    }
    return best, stats

def genetic_algorithm_visual(n, goal, heuristic=h_misplaced,
    pop_size=50, generations=200, crossover_rate=0.9, mutation_rate=0.1,
    return_steps=False, return_stats=False, return_logs=False
):
    start_time = time.time()
    goal = list(goal) if isinstance(goal, tuple) else goal

    population = [random.sample(range(n), n) for _ in range(pop_size)]

    steps_visual = []
    logs = []
    expanded = len(population)
    visited = 0
    result = None

    for g in range(1, generations + 1):
        best_curr = min(population, key=lambda s: heuristic(s, goal))
        h_best = heuristic(best_curr, goal)
        steps_visual.append(best_curr[:])
        show = ""
        show += f"Gen {g}. Pops: {population}"
        logs.append(show)
        # Kiểm tra goal
        for s in population:
            visited += 1
            if s == goal:
                result = s
                show += f"GOAL: {s}"
                logs.append(show)
                elapsed = (time.time() - start_time) * 1000
                stats = {
                    "expanded": expanded,
                    "visited": visited,
                    "frontier": 0,
                    "time": elapsed
                }
                if return_stats and return_logs:
                    return s, steps_visual, stats, logs
                elif return_logs:
                    return s, steps_visual, logs
                elif return_stats:
                    return s, steps_visual, stats
                return (s, steps_visual) if return_steps else s

        # Sinh thế hệ mới
        new_pop = []
        while len(new_pop) < pop_size:
            p1 = tournament_selection(population, goal, heuristic)
            p2 = tournament_selection(population, goal, heuristic)

            if random.random() < crossover_rate:
                c1 = order_crossover(p1, p2)
                c2 = order_crossover(p2, p1)
            else:
                c1, c2 = p1[:], p2[:]

            c1 = mutate(c1, mutation_rate)
            c2 = mutate(c2, mutation_rate)

            new_pop.extend([c1, c2])
            expanded += 2

        population = new_pop

    # Kết thúc sau khi hết thế hệ
    elapsed = (time.time() - start_time) * 1000
    best = result if result else min(population, key=lambda s: heuristic(s, goal))
    h_best = heuristic(best, goal)
    logs.append(f"No goal found after {generations} generations.")
    logs.append(f"Best found: {best} | h={h_best}")

    stats = {
        "expanded": expanded,
        "visited": visited,
        "frontier": 0,
        "time": elapsed
    }

    if return_stats and return_logs:
        return best, steps_visual, stats, logs
    elif return_logs:
        return best, steps_visual, logs
    elif return_stats:
        return best, steps_visual, stats
    return (best, steps_visual) if return_steps else best