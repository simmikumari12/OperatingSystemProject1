import copy
from process_generator import generate_processes
from ComputeMetrix import metrics, format_cycles

# -------------------------
# Q3: Memory-Aware Heterogeneous Scheduling
# Processors: PA PB PC = 2 GHz, 8GB RAM
#             PD PE PF = 4 GHz, 16GB RAM
# A process can only run on a node with enough memory.
# Strategy: extend Q2 greedy scheduler with memory check before assignment.
# -------------------------

PROCESSORS = [
    {"name": "PA", "speed": 2, "memory": 8  * 1024**3, "finish": 0.0},
    {"name": "PB", "speed": 2, "memory": 8  * 1024**3, "finish": 0.0},
    {"name": "PC", "speed": 2, "memory": 8  * 1024**3, "finish": 0.0},
    {"name": "PD", "speed": 4, "memory": 16 * 1024**3, "finish": 0.0},
    {"name": "PE", "speed": 4, "memory": 16 * 1024**3, "finish": 0.0},
    {"name": "PF", "speed": 4, "memory": 16 * 1024**3, "finish": 0.0},
]

def memory_aware_schedule(processes):
    procs = copy.deepcopy(PROCESSORS)
    completion = []
    skipped = []

    # Sort largest burst first so fastest cores get heaviest jobs
    sorted_procs = sorted(processes, key=lambda x: x.burst, reverse=True)

    for p in sorted_procs:
        # Find all processors with enough memory
        eligible = [pr for pr in procs if pr["memory"] >= p.memory]

        if not eligible:
            # No processor can fit this process — skip it
            skipped.append(p.pid)
            completion.append(None)
            continue

        # Among eligible processors, pick the one that minimizes finish time
        # (burst / speed gives execution time in cycles-per-GHz units)
        best = min(eligible, key=lambda pr: pr["finish"] + (p.burst / pr["speed"]))
        finish = best["finish"] + (p.burst / best["speed"])
        best["finish"] = finish
        completion.append(finish)

    # Re-align to original process order (pid == original index)
    aligned = [None] * len(processes)
    for i, p in enumerate(sorted_procs):
        aligned[p.pid] = completion[i]

    return aligned, skipped

def metrics_q3(processes, completion):
    total_wait = 0
    total_turn = 0
    count = 0
    for i, p in enumerate(processes):
        if completion[i] is None:
            continue
        turnaround = completion[i]
        waiting = turnaround - p.burst
        total_turn += turnaround
        total_wait += waiting
        count += 1
    return total_wait / count, total_turn / count

if __name__ == "__main__":
    processes = generate_processes(n=250, seed=42)
    print("Running Q3 Memory-Aware Heterogeneous Scheduling...\n")

    completion_q3, skipped = memory_aware_schedule(processes)

    wait_q3, turn_q3 = metrics_q3(processes, completion_q3)

    print("--- Q3 RESULTS ---")
    print(f"Processes scheduled : {250 - len(skipped)} / 250")
    if skipped:
        print(f"Skipped (no fit)    : {len(skipped)} processes (memory > 16GB)")
    print(f"Average Waiting Time  : {format_cycles(wait_q3)}")
    print(f"Average Turnaround    : {format_cycles(turn_q3)}")

    print("\n--- COMPARISON: Q2 vs Q3 ---")
    print(f"{'Metric':<25} {'Q2 (no memory)':>18} {'Q3 (memory-aware)':>20}")
    print("-" * 65)
    print(f"{'Avg Turnaround':<25} {'22.550T cycles':>18} {format_cycles(turn_q3):>20}")
    print(f"{'Avg Wait':<25} {'21.248T cycles':>18} {format_cycles(wait_q3):>20}")