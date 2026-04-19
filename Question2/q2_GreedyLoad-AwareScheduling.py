import copy
from process_generator import generate_processes
from ComputeMetrix import metrics, format_cycles

# -------------------------
# Q2: Heterogeneous Scheduling
# Processors: PA PB PC = 2 GHz (slow), PD PE PF = 4 GHz (fast)
# Strategy: sort by burst descending, assign longest jobs to fastest cores.
# Fast cores run at 2x speed, so divide burst by 2 for their time cost.
# -------------------------
def heterogeneous_schedule(processes):
    slow = [0, 0, 0]   # PA PB PC @ 2 GHz — full burst time
    fast = [0, 0, 0]   # PD PE PF @ 4 GHz — burst / 2 time

    completion = []

    # Sort largest burst first so fast cores get the heaviest jobs
    sorted_procs = sorted(processes, key=lambda x: x.burst, reverse=True)

    # Midpoint of the correct burst range (10M to 10T) = 5*10^11
    THRESHOLD = 5 * 10**11

    for p in sorted_procs:
        if p.burst > THRESHOLD:
            # Long job — must go to a fast core
            idx = fast.index(min(fast))
            finish = fast[idx] + (p.burst / 2)
            fast[idx] = finish
        else:
            # Short job — pick whichever core (fast or slow) is free soonest
            best_fast_time = min(fast) + (p.burst / 2)
            best_slow_time = min(slow) + p.burst
            if best_fast_time <= best_slow_time:
                idx = fast.index(min(fast))
                finish = fast[idx] + (p.burst / 2)
                fast[idx] = finish
            else:
                idx = slow.index(min(slow))
                finish = slow[idx] + p.burst
                slow[idx] = finish

        completion.append(finish)

    # Re-align completion list to original process order
    order = {p.pid: i for i, p in enumerate(sorted_procs)}
    aligned = [0] * len(processes)
    for i, p in enumerate(sorted_procs):
        orig_idx = p.pid  # pid == original index since we generate 0..249
        aligned[orig_idx] = completion[i]

    return aligned

if __name__ == "__main__":
    processes = generate_processes(n=250, seed=42)
    print("Running Q2 Heterogeneous Scheduling...\n")

    procs_q2 = copy.deepcopy(processes)
    completion_q2 = heterogeneous_schedule(procs_q2)
    wait_q2, turn_q2 = metrics(procs_q2, completion_q2)

    print("--- Q2 RESULTS ---")
    print(f"Average Waiting Time  : {format_cycles(wait_q2)}")
    print(f"Average Turnaround    : {format_cycles(turn_q2)}")