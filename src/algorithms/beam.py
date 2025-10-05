import random, time
from .heuristic import h_misplaced

def successors(state, n):
    succ = []
    for i in range(n):
        for j in range(n):
            if j != state[i]:
                s = state[:]
                s[i] = j
                succ.append(s)
    return succ

def beam_search(n, goal, return_steps=False, return_stats=False,
                beam_width=10, max_steps=1000, heuristic=h_misplaced):
    """
    Beam Search có thống kê tương tự BFS, nhưng frontier thường nhỏ.
    """
    start_time = time.time()

    beam = [random.sample(range(n), n) for _ in range(beam_width)]
    steps_visual = []
    steps_beam = []

    expanded = 0
    visited = 0

    for step in range(1, max_steps + 1):
        steps_beam.append([s[:] for s in beam])

        # Kiểm tra goal trong beam
        for s in beam:
            visited += 1
            if s == goal:
                elapsed = (time.time() - start_time) * 1000
                stats = {
                    "expanded": expanded,
                    "visited": visited,
                    "frontier": len(beam),
                    "time": elapsed
                }
                if return_stats:
                    if return_steps:
                        return s, steps_visual, stats
                    return s, stats
                if return_steps:
                    return s, steps_visual, steps_beam
                return s

        all_succ = []
        for s in beam:
            succ = successors(s, n)
            all_succ.extend(succ)
            expanded += len(succ)
            steps_visual.extend(succ)

        if not all_succ:
            break

        beam = sorted(all_succ, key=lambda s: heuristic(s, goal))[:beam_width]

    elapsed = (time.time() - start_time) * 1000
    best = min(beam, key=lambda s: heuristic(s, goal))
    stats = {
        "expanded": expanded,
        "visited": visited,
        "frontier": len(beam),
        "time": elapsed
    }

    if return_stats:
        if return_steps:
            return best, steps_visual, stats
        return best, stats
    if return_steps:
        return best, steps_visual, steps_beam
    return best
