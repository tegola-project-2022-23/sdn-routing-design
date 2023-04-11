import csv
import os
import numpy as np

def downstream_adjustment(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=" ")
        for row in reader:
            array = np.array(row)[:-1]
            return np.reshape(array, (12,12))

def write_demand(matrix, filename):
    with open(filename, 'w') as file:
        for i in range(13):
            for j in range(13):
                file.write(str(matrix[i][j]) + " ")
        file.write("\n")

if __name__ == "__main__":
    array = downstream_adjustment("max_demands.txt")
    # take the important column/row for demands
    upstream_demand = array[:,10]
    downstream_demand = array[10, :]
    # -1 accounts for the base 0 arrays
    reorder_index = np.array([11,12,1,4,5,7,8,2,6,10,9,3]) - 1
    # reorder the column to our new node ordering as defined in the draw.io diagrams
    upstream_column = [upstream_demand[reorder_index[i]] for i in range(12)]
    downstream_column = [downstream_demand[reorder_index[i]] for i in range(12)]
    upstream_column = np.insert(upstream_column, 0, 0.0)
    downstream_column = np.insert(downstream_column, 0, 0.0)
    # build a demand matrix in each direction
    reordered_upstream = np.zeros(shape=(13,13))
    reordered_downstream = np.zeros(shape=(13,13))
    reordered_upstream[:, 0] = upstream_column
    reordered_downstream[0] = downstream_column

    write_demand(reordered_downstream, "downstream-demand.txt")
    write_demand(reordered_upstream, "upstream-demand.txt")