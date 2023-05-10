import csv
from Process import Process


class InputReader:
    @classmethod
    def read_input(cls, filename):
        list_of_processes = []
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['pre_processes'].split(";") == ['']:
                    pre_process = []
                else:
                    pre_process = row['pre_processes'].split(";")
                list_of_processes.append(Process(row['process'], int(row['time']), pre_process))
        return list_of_processes
