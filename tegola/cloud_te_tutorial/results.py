from NetworkTopology import *
from NetworkParser import *
from TESolver import *
from MIPSolver import *
from helper import *

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

if __name__ == "__main__":
    base_network = network("b4", "topology.txt")
    base_network.setup("demand.txt")
    base_network.basic_solve()
    print(base_network.get_allocations())