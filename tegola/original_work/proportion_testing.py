from prelim_calculations import Calculate
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import csv
from demand_calculation import *
import os

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

if __name__ == "__main__":
    filename = "demands/max_demands.txt"

    name = ["demands" + str(i) for i in range(101)]

    for i in range(101):

        list = []

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

        

