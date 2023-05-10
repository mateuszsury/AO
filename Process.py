class Process:
    def __init__(self, name, time, pre_process):
        self.name = name
        self.time = time
        self.pre_process = pre_process
        if not pre_process:
            self.ready = True
        else:
            self.ready = False

    def change_ready(self):
        if not self.pre_process:
            self.ready = True
        else:
            self.ready = False

    def delete_pre_process(self, to_delete):
        if to_delete.name in self.pre_process:
            self.pre_process.remove(to_delete.name)
            self.change_ready()

    def __str__(self):
        return f'({self.name} {self.time})'
    
    def __iter__(self):
        return iter([self.name, self.time])

