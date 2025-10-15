import random, time
from .heuristic import h_misplaced

def successors(state, n):
    succ = []
    if len(state) < n:
        for j in range(n):
            if j not in state:
                succ.append(state + [j])
    else:
        return []
    return succ

def beam_search(n, goal, beam_width=10, max_steps=1000, heuristic=h_misplaced):
    start_time = time.time()

    beam = [[]]
    expanded = 0
    visited = 0

    for step in range(1, max_steps + 1):
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
                return s, stats

        all_succ = []
        for s in beam:
            succ = successors(s, n)
            all_succ.extend(succ)
            expanded += len(succ)

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
    return best, stats

def beam_search_visual(n, goal, beam_width=10, max_steps=1000, heuristic=h_misplaced,
    return_steps=False, return_stats=False, return_logs=False
):
    start_time = time.time()
    goal = list(goal) if isinstance(goal, tuple) else goal

    beam = [[]]
    steps_visual = []
    logs = []
    expanded = 0
    visited = 0

    for step in range(1, max_steps + 1):
        new_beam = []
        show = ""
        show += f"Beam: {beam}"
        logs.append(show)
        for s in beam:
            steps_visual.append(s)
            visited += 1

            if s == goal:
                elapsed = (time.time() - start_time) * 1000
                stats = {
                    "expanded": expanded,
                    "visited": visited,
                    "frontier": len(beam),
                    "time": elapsed
                }
                logs.append(f"GOAL FOUND at step {step}: {s}")
                if return_stats and return_logs:
                    return s, steps_visual, stats, logs
                elif return_logs:
                    return s, steps_visual, logs
                elif return_stats:
                    return s, steps_visual, stats
                return (s, steps_visual) if return_steps else s

            succ = successors(s, n)
            expanded += len(succ)
            if succ:
                new_beam.extend(succ)

        if not new_beam:
            logs.append("No more successors — stopping search.")
            break

        ranked = sorted(new_beam, key=lambda s: heuristic(s, goal))
        beam = ranked[:beam_width]

    elapsed = (time.time() - start_time) * 1000
    best = min(beam, key=lambda s: heuristic(s, goal)) if beam else []
    logs.append(f"Best found: {best} | h={heuristic(best, goal)}")

    stats = {
        "expanded": expanded,
        "visited": visited,
        "frontier": len(beam),
        "time": elapsed
    }

    if return_stats and return_logs:
        return best, steps_visual, stats, logs
    elif return_logs:
        return best, steps_visual, logs
    elif return_stats:
        return best, steps_visual, stats
    return (best, steps_visual) if return_steps else best