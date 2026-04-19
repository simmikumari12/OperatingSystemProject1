from FIFO import fifo

def sjf(processes, num_procs=6):
    processes = sorted(processes, key=lambda x: x.burst)
    return fifo(processes, num_procs)