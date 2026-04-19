import random

class Process:
    def __init__(self, pid, burst, memory):
        self.pid = pid
        self.burst = burst
        self.memory = memory
        self.remaining = burst

processes = []
for i in range(250):
    burst = random.randint(10**6, 10**8)   # reduce range for runtime
    memory = random.randint(1, 16)         # in GB
    processes.append(Process(i, burst, memory))