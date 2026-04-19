from collections import deque

def rr(processes, quantum=None, num_procs=6):
    # Default quantum = mean burst / 10 (scales correctly with any burst range)
    if quantum is None:
        mean_burst = sum(p.burst for p in processes) // len(processes)
        quantum = mean_burst // 10

    queue = deque(processes)
    time = [0] * num_procs
    completion = {}

    while queue:
        for i in range(num_procs):
            if not queue:
                break
            p = queue.popleft()
            exec_time = min(quantum, p.remaining)
            time[i] += exec_time
            p.remaining -= exec_time
            if p.remaining == 0:
                completion[p.pid] = time[i]
            else:
                queue.append(p)

    return [completion[i] for i in range(len(processes))]