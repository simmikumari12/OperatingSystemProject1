def metrics(processes, completion):
    total_wait = 0
    total_turn = 0
    for i, p in enumerate(processes):
        turnaround = completion[i]
        waiting = turnaround - p.burst
        total_turn += turnaround
        total_wait += waiting
    return total_wait / len(processes), total_turn / len(processes)

def format_cycles(c):
    if c >= 1e12:
        return f"{c/1e12:.3f}T cycles"
    elif c >= 1e9:
        return f"{c/1e9:.3f}B cycles"
    elif c >= 1e6:
        return f"{c/1e6:.3f}M cycles"
    return f"{c:,.0f} cycles"
