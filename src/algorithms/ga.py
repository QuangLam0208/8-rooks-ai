import random
from .heuristic import h_misplaced   # hoặc h_partial

def fitness(state, goal, heuristic):
    """
    Chuyển heuristic (h càng nhỏ càng tốt) -> fitness (càng lớn càng tốt)
    Ở đây: fitness = -h
    """
    return -heuristic(state, goal)

def tournament_selection(pop, goal, heuristic, k=3):
    """
    Chọn 1 cá thể tốt nhất trong k cá thể ngẫu nhiên
    => cá thể có h nhỏ nhất (fitness cao nhất).
    """
    return max(random.sample(pop, k), key=lambda s: fitness(s, goal, heuristic))

def order_crossover(p1, p2):
    """Order Crossover (OX) giữ dạng hoán vị"""
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
    """Đột biến: hoán đổi 2 vị trí"""
    s = state[:]
    if random.random() < rate:
        i, j = random.sample(range(len(s)), 2)
        s[i], s[j] = s[j], s[i]
    return s

def genetic_algorithm(n, goal, heuristic=h_misplaced,
                      pop_size=50, generations=500,
                      crossover_rate=0.9, mutation_rate=0.1):
    """
    GA sử dụng heuristic h(state, goal) (càng nhỏ càng tốt).
    """
    # 1. Khởi tạo quần thể ban đầu (các hoán vị cột)
    population = [random.sample(range(n), n) for _ in range(pop_size)]

    for g in range(1, generations + 1):
        # Kiểm tra xem có cá thể nào = goal chưa
        for s in population:
            if s == goal:
                # print(f"Goal found at generation {g}: {s}")
                return s

        # 2. Sinh thế hệ mới
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

        population = new_pop

    # Hết thế hệ mà chưa gặp goal
    best = min(population, key=lambda s: heuristic(s, goal))
    print(f"No exact goal after {generations} generations.")
    print(f"Best found: {best} (h={heuristic(best, goal)})")
    return best