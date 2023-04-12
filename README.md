# sdn-routing-design
Approaching the challenge of revisiting routing in the Tegola network with a high-level Switch view, and using global information about the network and its traffic to make informed routing decisions

File descriptions:

prelim_calculations.py - helper file for data analysis. Performs some data cleaning and gathering from Zabbix.

demand_calculation.py - data gathering for the demand matrix used in the data analysis

data_analysis.ipynb - original analysis of data in the tegola network taken towards the start of the project

final_data.ipynb - updated data analysis that is represented in the final report

proportion_testing.py - previous testing for proportional splits on an earlier version of the implementation

results.py - implementation of the algorithmic solution, and production of the results for chapter 5

TESolver.py, MIPSolver.py, NetworkParser.py, NetworkTopology.py, helper.py, traffic_eng_init.ipynb - files adapted from the Rachee Singh Cloud TE Tutorial https://github.com/racheesingh/cloud-te-tutorial
