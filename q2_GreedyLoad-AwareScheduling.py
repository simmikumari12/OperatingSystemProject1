import random
import copy

# -------------------------
# Process Definition
# -------------------------
class Process:
    def __init__(self, pid, burst, memory):
        self.pid = pid
        self.burst = burst
        self.memory = memory

# -------------------------
# Generate Processes
# -------------------------
processes = []
for i in range(250):
    burst = random.randint(10**6, 10**8)
    memory = random.randint(1, 16)
    processes.append(Process(i, burst, memory))

# -------------------------
# Metrics Function
# -------------------------
def metrics(processes, completion):
    total_wait = 0
    total_turn = 0

    for i, p in enumerate(processes):
        turnaround = completion[i]
        waiting = turnaround - p.burst

        total_turn += turnaround
        total_wait += waiting

    return total_wait / len(processes), total_turn / len(processes)

# -------------------------
# Q2: Heterogeneous Scheduling
# -------------------------
def heterogeneous_schedule(processes):

    slow = [0, 0, 0]   # PA PB PC (2 GHz)
    fast = [0, 0, 0]   # PD PE PF (4 GHz)

    completion = []

    # Sort by burst time (largest first)
    processes = sorted(processes, key=lambda x: x.burst, reverse=True)

    for p in processes:

        # Assign long jobs to fast cores
        if p.burst > 5 * 10**7:
            idx = fast.index(min(fast))
            finish = fast[idx] + (p.burst / 2)
            fast[idx] = finish

        else:
            # choose best available core
            if min(fast) <= min(slow):
                idx = fast.index(min(fast))
                finish = fast[idx] + (p.burst / 2)
                fast[idx] = finish
            else:
                idx = slow.index(min(slow))
                finish = slow[idx] + p.burst
                slow[idx] = finish

        completion.append(finish)

    return completion

# -------------------------
# MAIN EXECUTION
# -------------------------
if __name__ == "__main__":

    print("Running Q2 Heterogeneous Scheduling...\n")

    procs_q2 = copy.deepcopy(processes)

    completion_q2 = heterogeneous_schedule(procs_q2)

    wait_q2, turn_q2 = metrics(procs_q2, completion_q2)

    print("--- Q2 RESULTS ---")
    print("Average Waiting Time:", wait_q2)
    print("Average Turnaround Time:", turn_q2)