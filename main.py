from InputReader import InputReader
from Machine import Machine
from MachineListMethods import MachineListMethods


def main():
    list_of_processes = InputReader.read_input("simple.csv")
    list_of_processes_meta = InputReader.read_input("simple.csv")
    list_of_processes.sort(key=lambda x: x.time, reverse=True)
    list_of_machines = []
    [list_of_machines.append(Machine()) for _ in range(3)]
    MachineListMethods.simulate(list_of_processes, list_of_machines)
    MachineListMethods.print(list_of_machines)
    MachineListMethods.export(list_of_machines)
    MachineListMethods.draw(list_of_machines)

    #LPT_no_relations
    list_of_processes_no_relations = InputReader.read_input("simple.csv")
    list_of_machines_no_relations = []
    [list_of_machines_no_relations.append(Machine()) for _ in range(3)]
    MachineListMethods.lpt_scheduling(list_of_processes_no_relations, list_of_machines_no_relations)
    MachineListMethods.print(list_of_machines_no_relations)
    MachineListMethods.export_no_rel(list_of_machines_no_relations, 'output.csv')
    #Simulated_annealing
    MachineListMethods.simulated_annealing(list_of_processes_no_relations, list_of_machines_no_relations, initial_temperature=1000, cooling_rate=0.99)
    MachineListMethods.print(list_of_machines_no_relations)
    MachineListMethods.export_no_rel(list_of_machines_no_relations, 'solution.csv')
    MachineListMethods.draw(list_of_machines_no_relations)

if __name__ == '__main__':
    main()


