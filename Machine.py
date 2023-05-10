class Machine:
    def __init__(self, in_job=False, end_time=0):
        self.in_job = in_job
        self.end_time = end_time
        self.processes = []
