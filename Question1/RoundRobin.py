from collections import deque

def rr(processes, quantum=1000, num_procs=6):
    queue = deque(processes)
    time = [0]*num_procs
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
