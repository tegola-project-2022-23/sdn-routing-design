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

    def scale_up_demands(self):
        return
    
    def write_demand(self, matrix, filename):
        with open(filename, 'w') as file:
            for i in range(11):
                for j in range(11):
                    file.write(str(matrix[i][j]) + " ")
            file.write("\n")

    def fix_demands(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter=" ")
            for row in reader:
                array = np.array(row)[:-1]
                new_array = np.reshape(array, (13,13))
                downstream_row = new_array[0][3:]
                upstream_col = new_array[:, 0][3:]
                upstream_col = np.insert(upstream_col, 0, 0.0)
                downstream_row = np.insert(downstream_row, 0, 0.0)
                reordered_upstream = np.zeros(shape=(11,11))
                reordered_downstream = np.zeros(shape=(11,11))
                reordered_upstream[:, 0] = upstream_col
                reordered_downstream[0] = downstream_row

                return reordered_downstream
    
if __name__ == "__main__":
    base_network = network("b4", "topology.txt")
    base_network.setup("demand.txt")
    base_network.basic_solve()
    print(base_network.get_allocations())
    matrix = base_network.fix_demands("downstream-demand.txt")
    base_network.write_demand(matrix, "hello.txt")