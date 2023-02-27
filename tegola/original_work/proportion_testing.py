import numpy as np
import matplotlib.pyplot as plt
from demand_calculation import *
from NetworkTopology import *
from NetworkParser import *
from TESolver import *
from MIPSolver import *
from helper import *

def read_input_file(filename, proportion_to_mhi):

    with open(filename, "r") as file:
        for line in file:
            entry = line.split(" ")
            entry = np.reshape(np.array([float(x) for x in entry[0:len(entry) - 1]]), (12,12))
            entry = perform_split(entry, proportion_to_mhi)
            return entry

def perform_split(matrix, proportion_to_mhi):
    # Some preprocessing due to an error in data collection
    for i in range(12):
        if i == 0 or i == 3:
            continue
        else:
            matrix[i][11] = matrix[i][10]
            matrix[i][10] = 0

            matrix[11][i] = matrix[10][i]
            matrix[10][i] = 0
        
    return split_improved(matrix, proportion_to_mhi)

def get_unmet_demands():

    dict = {}

    for index in range(101):
        network_name = "b4"
        network = parse_topology(network_name)
        parse_demands(index, network)
        parse_tunnels(network)
        initialize_weights(network)

        mip = CvxSolver()
        solver = TESolver(mip, network)
        solver.add_demand_constraints()
        solver.add_edge_capacity_constraints()
        solver.Maximize(get_max_flow_objective(network))

        max_flow = solver.solve()
        unmet_demands = sum(get_demands_unmet(network).values())
        print(unmet_demands)
        dict[index] = unmet_demands

    return dict

def setup_demand_files():
    filename = "demands/max_demands.txt"
    name = ["demands" + str(i) for i in range(101)]

    for i in range(101):
        if i == 0:
            index = 0
        else:
            index = i * 0.01
        
        with open("demands/" + name[i] + ".txt", "w") as file:
            entry = read_input_file(filename, index)
            for i in range(12):
                for j in range(12):
                    file.write(str(entry[i][j]) + " ")
            file.write("\n")
    return

if __name__ == "__main__":
    dict = get_unmet_demands()
    keys = np.array(list(dict.keys()))
    values = np.array(list(dict.values()))
    fig, ax = plt.subplots(1, 1, figsize=(6,6))
    ax.plot(keys[7:30], values[7:30])
    ax.set_title("Unmet demands for varying proportions of traffic sent to MHI")
    ax.set_xlabel("Traffic to MHI (%)")
    ax.set_ylabel("Unmet Demands (Mb)")
    plt.show()

    # The region of 15-23% appears to be the best split for Tegola's demands

        

