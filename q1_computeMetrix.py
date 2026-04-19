def metrics(processes, completion):
    total_wait = 0
    total_turn = 0

    for i, p in enumerate(processes):
        turnaround = completion[i]
        waiting = turnaround - p.burst

        total_turn += turnaround
        total_wait += waiting

    return total_wait/len(processes), total_turn/len(processes)

