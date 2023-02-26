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
            list.append(entry)
    return list


if __name__ == "__main__":
    filename = "thirty_seventy.txt"
    list = read_input_file(filename)
    print(list)
