from prelim_calculations import Calculate
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import csv
from demand_calculation import *
import os

def read_input_file(filename):
    list = []
    with open(filename, "r") as file:
        for line in file:
            line = file.readline()
            entry = line.split(" ")
            entry = np.reshape(np.array([float(x) for x in entry[0:len(entry) - 1]]), (12,12))

            entry = return_to_original(entry)
            print(entry)
            list.append(entry)
    return list

def return_to_original(matrix):
    for i in range(12):
        if i == 0 or i == 3:
            matrix[i][10] = matrix[i][10] + matrix[i][11]
            matrix[i][11] = 0

            matrix[10][i] = matrix[10][i] + matrix[11][i]
            matrix[11][i] = 0
        else:
            matrix[i][11] = matrix[i][10] + matrix[i][11]
            matrix[i][10] = 0

            matrix[11][i] = matrix[10][i] + matrix[11][i]
            matrix[10][i] = 0
    return matrix

if __name__ == "__main__":
    filename = "thirty_seventy.txt"
    list = read_input_file(filename)
