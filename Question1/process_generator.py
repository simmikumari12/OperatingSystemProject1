import random
import math

class Process:
    def __init__(self, pid, burst, memory):
        self.pid = pid
        self.burst = burst          # CPU cycles
        self.memory = memory        # bytes
        self.remaining = burst

def clamp(val, lo, hi):
    return max(lo, min(hi, val))

def generate_processes(n=250, seed=42):
    random.seed(seed)
    processes = []
    for i in range(n):
        # Burst: 10*10^6 to 10*10^12 cycles (log-normal so spread is realistic)
        lo_b = 10 * 10**6
        hi_b = 10 * 10**12
        burst = int(clamp(random.lognormvariate(math.log(5e11), 1.5), lo_b, hi_b))

        # Memory: 1MB to 16GB in bytes (log-normal, right-skewed)
        lo_m = 1 * 1024**2
        hi_m = 16 * 1024**3
        memory = int(clamp(random.lognormvariate(math.log(500 * 1024**2), 1.2), lo_m, hi_m))

        processes.append(Process(i, burst, memory))
    return processes

# Default shared process list
processes = generate_processes()