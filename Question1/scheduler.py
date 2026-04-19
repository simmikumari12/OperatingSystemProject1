import copy
from process_generator import generate_processes
from FIFO import fifo
from q1_SJF import sjf
from RoundRobin import rr
from ComputeMetrix import metrics, format_cycles

if __name__ == "__main__":
    processes = generate_processes(n=250, seed=42)
    print(f"Loaded {len(processes)} processes")
    print(f"Burst range: {min(p.burst for p in processes):,} – {max(p.burst for p in processes):,} cycles")
    print(f"Memory range: {min(p.memory for p in processes)//1024**2} MB – {max(p.memory for p in processes)//1024**3} GB\n")

    # FIFO
    p1 = copy.deepcopy(processes)
    c1 = fifo(p1)
    w1, t1 = metrics(p1, c1)

    # SJF
    p2 = copy.deepcopy(processes)
    c2 = sjf(p2)
    w2, t2 = metrics(p2, c2)

    # Round Robin
    p3 = copy.deepcopy(processes)
    c3 = rr(p3)
    w3, t3 = metrics(p3, c3)

    print("--- RESULTS ---")
    print(f"{'Algorithm':<12} {'Avg Wait':>20} {'Avg Turnaround':>22}")
    print("-" * 56)
    for name, w, t in [("FIFO", w1, t1), ("SJF", w2, t2), ("RR", w3, t3)]:
        print(f"{name:<12} {format_cycles(w):>20} {format_cycles(t):>22}")

    