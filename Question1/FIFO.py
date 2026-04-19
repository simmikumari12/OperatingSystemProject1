def fifo(processes, num_procs=6):
    time = [0] * num_procs
    completion = []
    for p in processes:
        idx = time.index(min(time))
        finish = time[idx] + p.burst
        time[idx] = finish
        completion.append(finish)
    return completion