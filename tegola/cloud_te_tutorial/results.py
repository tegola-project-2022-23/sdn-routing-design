from NetworkTopology import *
from NetworkParser import *
from TESolver import *
from MIPSolver import *
from helper import *
import numpy as np

class network:
    
    def __init__(self, net_name, topo_filename):
        self.network_name = net_name
        self.network = parse_topology(self.network_name, topo_filename)
        self.allocations = {}

    def setup(self, demand_filename):
        parse_demands(self.network, demand_filename)
        parse_tunnels(self.network)
        initialize_weights(self.network)
        self.G = self.network.to_nx()
        self.capacity_labels = { edge : self.network.edges[edge].capacity for edge in self.G.edges } 

    def basic_solve(self):
        mip = CvxSolver()
        solver = TESolver(mip, self.network)
        solver.add_demand_constraints()
        solver.add_edge_capacity_constraints()
        solver.Maximize(get_max_flow_objective(self.network))
        max_flow = solver.solve()

    def get_allocations(self):
        return get_edge_flow_allocations(self.network)
    
    def write_demand(self, matrix, filename):
        with open("data/tegola/" + filename, 'w') as file:
            for i in range(11):
                for j in range(11):
                    file.write(str(matrix[i][j]) + " ")
            file.write("\n")

    def fix_demands_downstream(self, filename, scale_factor):
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter=" ")
            for row in reader:
                array = np.array(row)[:-1]
                new_array = np.reshape(array, (13,13))
                downstream_row = new_array[0][3:]
                downstream_row = np.insert(downstream_row, 0, 0.0)
                reordered_downstream = np.zeros(shape=(11,11))
                reordered_downstream[0] = downstream_row

                return reordered_downstream * scale_factor

    def fix_demands_upstream(self, filename, scale_factor):
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter=" ")
            for row in reader:
                array = np.array(row)[:-1]
                new_array = np.reshape(array, (13,13))
                upstream_col = new_array[:, 0][3:]
                upstream_col = np.insert(upstream_col, 0, 0.0)
                reordered_upstream = np.zeros(shape=(11,11))
                reordered_upstream[:, 0] = upstream_col

                return reordered_upstream * scale_factor
    
    # Overarching method for taking a 13x13 input and making it 11x11, then writing it to a file
    def fix_demands(self, downstream_file, upstream_file):
        down_target_file = "max_demand_downstream.txt"
        up_target_file = "max_demand_upstream.txt"
        scale_factor = 1
        downstream_matrix = base_network.fix_demands_downstream(downstream_file, scale_factor)
        upstream_matrix = base_network.fix_demands_upstream(upstream_file, scale_factor)
        self.write_demand(downstream_matrix, down_target_file)
        self.write_demand(upstream_matrix, up_target_file)

    def even_allocations(self):
        return


if __name__ == "__main__":
    base_network = network("tegola", "topology.txt")
    base_network.setup("demand.txt")
    base_network.basic_solve()
    base_network.fix_demands("downstream-demand.txt", "upstream-demand.txt")
    base_network.allocations = base_network.get_allocations()
    print(base_network.allocations)