import random
import copy
from collections import deque

# -------------------------
# Process Class
# -------------------------
class Process:
    def __init__(self, pid, burst, memory):
        self.pid = pid
        self.burst = burst
        self.memory = memory
        self.remaining = burst

# -------------------------
# Generate Processes
# -------------------------
processes = []
for i in range(250):
    burst = random.randint(10**6, 10**8)
    memory = random.randint(1, 16)
    processes.append(Process(i, burst, memory))

# -------------------------
# Scheduling Algorithms
# -------------------------
def fifo(processes, num_procs=6):
    time = [0]*num_procs
    completion = []

    for p in processes:
        idx = time.index(min(time))
        finish = time[idx] + p.burst
        time[idx] = finish
        completion.append(finish)

    return completion


def sjf(processes, num_procs=6):
    processes = sorted(processes, key=lambda x: x.burst)
    return fifo(processes, num_procs)


def rr(processes, quantum=100000, num_procs=6):
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

# -------------------------
# Metrics
# -------------------------
def metrics(processes, completion):
    total_wait = 0
    total_turn = 0

    for i, p in enumerate(processes):
        turnaround = completion[i]
        waiting = turnaround - p.burst

        total_turn += turnaround
        total_wait += waiting

    return total_wait/len(processes), total_turn/len(processes)

# -------------------------
# MAIN (THIS WAS MISSING)
# -------------------------
if __name__ == "__main__":

    p1 = copy.deepcopy(processes)
    c1 = fifo(p1)
    w1, t1 = metrics(p1, c1)

    p2 = copy.deepcopy(processes)
    c2 = sjf(p2)
    w2, t2 = metrics(p2, c2)

    p3 = copy.deepcopy(processes)
    c3 = rr(p3)
    w3, t3 = metrics(p3, c3)

    print("\n--- RESULTS ---")
    print(f"FIFO -> Avg Waiting: {w1}, Avg Turnaround: {t1}")
    print(f"SJF  -> Avg Waiting: {w2}, Avg Turnaround: {t2}")
    print(f"RR   -> Avg Waiting: {w3}, Avg Turnaround: {t3}")


    