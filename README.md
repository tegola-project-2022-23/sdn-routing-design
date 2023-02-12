# sdn-routing-design
Approaching the challenge of revisiting routing in the Tegola network with a high-level Switch view, and using global information about the network and its traffic to make informed routing decisions
# File Descriptions

demand_calculation.py - interacts with Zabbix Monitoring Software to retrieve traffic demands of source-destination node pairs in Tegola. Also implements splitting mechanism to produce arbitrary traffic split proportions between the two Tegola gateways. Produces output file demand.txt, a space-separated list of the demands in the most recent router poll which can be fed into the Cloud TE Tutorial's max-flow formulations.

prelim_calculations.py - performs the necessary data gathering and cleaning prior to analyising and visualising it in data_analysis.ipynb.

data_analysis.ipynb - produces statistics and visualisations about traffic patterns in the Tegola network. This file will provide the basis for the first proper thesis chapter (Motivation/Data Analysis). 
