import math
import random
import csv
from queue import PriorityQueue
from Process import Process
import matplotlib.pyplot as plt

class MachineListMethods:
    @classmethod
    def simulate(cls, list_of_processes, list_of_machines):
        priority_queue = PriorityQueue()
        counter_of_tasks = len(list_of_processes)
        for process in list_of_processes:
            if process.ready:
                priority_queue.put((-1 * process.time, process))
                list_of_processes.remove(process)
        global_time = 0
        while counter_of_tasks:
            if priority_queue.empty():
                min_time = math.inf
                min_index = 0
                for i, machine in enumerate(list_of_machines):
                    if machine.in_job:
                        if min_time > machine.end_time:
                            min_time = machine.end_time
                            min_index = i
                cls.finish_process_and_add_to_queue(list_of_machines, list_of_processes, min_index, priority_queue)
                global_time = min_time
            else:
                min_time = math.inf
                min_index = 0
                empty_machine = False
                for i, machine in enumerate(list_of_machines):
                    if min_time > machine.end_time:
                        min_time = machine.end_time
                        min_index = i
                    if not machine.in_job:
                        empty_machine = True
                if not empty_machine:
                    cls.finish_process_and_add_to_queue(list_of_machines, list_of_processes, min_index, priority_queue)
                    global_time = min_time
                new_process = priority_queue.get()[1]
                if global_time - list_of_machines[min_index].end_time > 0:
                    list_of_machines[min_index].processes.append(
                        Process("Break", global_time - list_of_machines[min_index].end_time, []))
                list_of_machines[min_index].processes.append(new_process)
                counter_of_tasks -= 1
                list_of_machines[min_index].in_job = True
                list_of_machines[min_index].end_time = global_time + new_process.time

    @classmethod
    def finish_process_and_add_to_queue(cls, list_of_machines, list_of_processes, min_index, priority_queue):
        process_delete = list_of_machines[min_index].processes[-1]
        list_of_machines[min_index].in_job = False
        for process in list_of_processes:
            process.delete_pre_process(process_delete)
            if process.ready:
                priority_queue.put((-1 * process.time, process))
                list_of_processes.remove(process)

    @classmethod
    def print(cls, list_of_machines):
        for i, machine in enumerate(list_of_machines):
            print(f'Machine number: {i + 1}')
            print(f'Machine time: {machine.end_time}')
            print("Machines processes:", end="")
            for process in machine.processes:
                print(process, end=" ")
            print()
            print()

    @classmethod
    def export(cls, list_of_machines):
        filename = 'data.csv'
        with open(filename, 'w', newline='') as file:
            data = csv.writer(file, delimiter = ';') #Eventually ','
            data.writerow(['Machine', 'Machine End Time', 'Procces (Time)'])
            for i, machine in enumerate(list_of_machines):
                row = [i+1, machine.end_time]
                for process in machine.processes:
                    row.extend(process)
                data.writerow(row)
    
    @classmethod
    def draw(cls, list_of_machines):
        fig, ax = plt.subplots()
        xscale = 0
        for i, machine in enumerate(list_of_machines):
            tasks = []
            current_time = 0
            if machine.end_time > xscale:
                xscale = machine.end_time
            for process in machine.processes:
                    tasks.append((process.name, current_time,current_time+ process.time))
                    current_time +=process.time
            for j, task in enumerate(tasks):
                if task[0] == "Break":
                    ax.barh(i, task[2] - task[1], left=task[1], height=0.6, align='center', color='white')
                else:
                    ax.barh(i, task[2] - task[1], left=task[1], height=0.6, align='center')
                ax.text(task[1] + (task[2] - task[1])/2, i - 0.2, task[0], ha='center', va='center')
                ax.text(task[1] + (task[2] - task[1])/2, i + 0.2, f"{task[2]-task[1]}", ha='center', va='center')
        #Set the Y-axis limits and labels
        ax.set_ylim(-1, len(list_of_machines))
        ax.set_yticks(range(len(list_of_machines)))
        ax.tick_params(axis='y', pad=2)
        ax.set_ylabel('Machine')
        # Set the X-axis limits and label
        ax.set_xlim(0, xscale)
        ax.set_xlabel('Time')
        plt.show()

    @classmethod
    def export_no_rel(cls, list_of_machines, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Machine', 'Machine End Time', 'Process'])
            for i, machine in enumerate(list_of_machines):
                row = [i + 1, machine.end_time]
                for process in machine.processes:
                    row.append(process)
                writer.writerow(row)

    @classmethod
    def lpt_scheduling(cls, list_of_processes, list_of_machines):
        sorted_processes = sorted(list_of_processes, key=lambda x: x.time, reverse=True)

        for process in sorted_processes:
            min_machine = min(list_of_machines, key=lambda x: x.end_time)
            min_machine.processes.append(process)
            min_machine.end_time += process.time

            for other_process in list_of_processes:
                if process.name in other_process.pre_process:
                    other_process.pre_process.remove(process.name)
                    if not other_process.pre_process:
                        other_process.ready = True


    @classmethod
    def simulated_annealing(cls, list_of_processes, list_of_machines, initial_temperature, cooling_rate):
        current_solution = list_of_processes
        best_solution = list_of_processes
        current_makespan = cls.calculate_makespan(list_of_machines)
        best_makespan = current_makespan
        temperature = initial_temperature

        while temperature > 1:
            new_solution = cls.generate_neighbour_solution(current_solution)
            new_makespan = cls.calculate_makespan(list_of_machines, new_solution)
            delta_makespan = new_makespan - current_makespan

            if delta_makespan < 0 or math.exp(-delta_makespan / temperature) > random.random():
                current_solution = new_solution
                current_makespan = new_makespan

                if current_makespan < best_makespan:
                    best_solution = current_solution
                    best_makespan = current_makespan

            temperature *= cooling_rate

        cls.assign_processes_to_machines(list_of_machines, best_solution)


    @classmethod
    def generate_neighbour_solution(cls, current_solution):
        neighbour_solution = current_solution[:]

        if len(neighbour_solution) > 1:
            index_1 = random.randint(0, len(neighbour_solution) - 1)
            index_2 = random.randint(0, len(neighbour_solution) - 1)

            neighbour_solution[index_1], neighbour_solution[index_2] = neighbour_solution[index_2], neighbour_solution[
                index_1]

        return neighbour_solution

    @classmethod
    def calculate_makespan(cls, list_of_machines, solution=None):
        if solution is None:
            solution = [process for machine in list_of_machines for process in machine.processes]

        cls.assign_processes_to_machines(list_of_machines, solution)

        return max(machine.end_time for machine in list_of_machines)

    @classmethod
    def assign_processes_to_machines(cls, list_of_machines, solution):
        for machine in list_of_machines:
            machine.processes.clear()
            machine.end_time = 0

        for process in solution:
            min_machine = min(list_of_machines, key=lambda x: x.end_time)
            min_machine.processes.append(process)
            min_machine.end_time += process.time