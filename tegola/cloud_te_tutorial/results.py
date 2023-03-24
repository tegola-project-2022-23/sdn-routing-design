from NetworkTopology import *
from NetworkParser import *
from TESolver import *
from MIPSolver import *
from helper import *
import numpy as np

class Solver:
    
    def __init__(self, net_name, topo_filename):
        self.network_name = net_name
        self.network = parse_topology(self.network_name, topo_filename)
        self.allocations = {}

    # Run setup for the network
    def setup(self, demand_filename):
        parse_demands(self.network, demand_filename)
        parse_tunnels(self.network)
        initialize_weights(self.network)
        self.G = self.network.to_nx()
        self.capacity_labels = { edge : self.network.edges[edge].capacity for edge in self.G.edges } 

    # Solve the network with demands and topology for basic flow allocations
    def basic_solve(self):
        mip = CvxSolver()
        solver = TESolver(mip, self.network)
        solver.add_demand_constraints()
        solver.add_edge_capacity_constraints()
        solver.Maximize(get_max_flow_objective(self.network))
        max_flow = solver.solve()

    def get_allocations(self):
        return get_edge_flow_allocations(self.network)
    
    # Write demands to data files in either up or downstream direction
    def write_demand(self, matrix, filename):
        with open("data/tegola/" + filename, 'w') as file:
            for i in range(11):
                for j in range(11):
                    file.write(str(matrix[i][j]) + " ")
            file.write("\n")

    # Convert 13x13 to 11x11 for new topology in downstream direction
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

    # Convert 13x13 to 11x11 for new topology in upstream direction
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
        down_target_file = "max_deself.edges = list(self.allocations.keys())mand_downstream.txt"
        up_target_file = "max_demand_upstream.txt"
        scale_factor = 1
        downstream_matrix = base.fix_demands_downstream(downstream_file, scale_factor)
        upstream_matrix = base.fix_demands_upstream(upstream_file, scale_factor)
        self.write_demand(downstream_matrix, down_target_file)
        self.write_demand(upstream_matrix, up_target_file)

    # Return the gateway edges in a network, given a sink node number and direction
    def get_gateway_edges(self, edges, sink, direction):
        if direction == "upstream":
            gateway_edges = [edge for edge in edges if edge[1] == str(sink)]
        elif direction == "downstream":
            gateway_edges = [edge for edge in edges if edge[0] == str(sink)]
        else:
            print("direction for getting gateway edges was not upstream or downstream")
            exit()
        return gateway_edges

    # Calculate the capacity for gateway edges in the basic 50/50 case
    def calculate_capacity(self, edges, sink, direction):
        gateway_edges = self.get_gateway_edges(edges, sink, direction)
        total_demand = sum([self.allocations.get(x) for x in gateway_edges])
        return total_demand / len(gateway_edges)

    # Reconfigure the topology file with the new capacities
    def set_new_capacities(self, sink, direction):
        edges = list(self.allocations.keys())
        gateway_edges = self.get_gateway_edges(edges, sink, direction)
        capacity = self.calculate_capacity(edges, sink, direction)

        for edge in gateway_edges:
            self.network.edges[edge].capacity = capacity

if __name__ == "__main__":

    # Setup the network
    base = Solver("tegola", "topology.txt")
    base.setup("demand.txt")

    #Generate basic flow allocations
    base.basic_solve()
    base.allocations = base.get_allocations()
    #####
    # This line can be uncommented to fix demands if necessary
    #base.fix_demands("downstream-demand.txt", "upstream-demand.txt")
    #####
    
    # Using basic allocations, recongiure the topology file to reflect the correct split
    base.set_new_capacities(1, "downstream")
    base.setup("demand.txt")
    base.basic_solve()
    new_allocations = base.get_allocations()
    print(new_allocations)

    # Re-run the max-flow solver with the new topology file to generate new allocations
    #print(base.network.edges[('1', '7')].capacity)