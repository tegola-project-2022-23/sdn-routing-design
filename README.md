# sdn-routing-design
Approaching the challenge of revisiting routing in the Tegola network with a high-level Switch view, and using global information about the network and its traffic to make informed routing decisions
# File Descriptions

demand_calculation.py - interacts with Zabbix Monitoring Software to retrieve traffic demands of source-destination node pairs in Tegola. Also implements splitting mechanism to produce arbitrary traffic split proportions between the two Tegola gateways. Produces output file demand.txt, a space-separated list of the demands in the most recent router poll which can be fed into the Cloud TE Tutorial's max-flow formulations.

prelim_calculations.py - performs the necessary data gathering and cleaning prior to analyising and visualising it in data_analysis.ipynb.

data_analysis.ipynb - produces statistics and visualisations about traffic patterns in the Tegola network. This file will provide the basis for the first proper thesis chapter (Motivation/Data Analysis). 


# Thesis Outline
Chapter 1 - Introduction (2-4 pages)

Brief section to begin the thesis that outlines the following:
- basic explanation of the problem we are trying to solve
- approach taken
- main achievements of the project
- summary of statistical results


Chapter 2 - Background (5-7 pages)

This section puts the project in context by examining Tegola's current setup and its shortcomings. Looking a little at the history of Internet access in Tegola to give context to how it currently operates. We perform a literature review, which is a detailed analysis of the relevant research in the areas related to our project. We use these research papers to show what has been done, and how we are adjusting/changing the scene to produce something new in this project.


Chapter 3 - Analysing Traffic Patterns of the Tegola Network (8-10 pages)

The first main section of the paper will be chapter 3, where we look in detail about the traffic patterns and demands that currently exist in Tegola. The main focus here will be to show how the current setup is not as efficient as it could be, with unequal gateway splitting, large disparity between demands to different switches and under-utilization of many links and paths in the network. Here we should focus on reproducible results over a long period of time (e.g. a month), and we would like to be able to compare the data in this section to some of our tests in the final chapter and show how we have improved the network.


Chapter 4 - Implementing Routing Heuristics to Improve Performance of the Tegola Network (10-12 pages)

This section will provide the implementation details of systems to effectively improve the performance metrics discussed in chapter 3. This could be split into a few different sections, perhaps with the first one discussing the proportional splitting of traffic between gateways, and the subsequent sections discussing the tweaks and improvements for the max-flow formulations.

Chapter 5 - Quantitative Analysis of Implemented Systems (8-10 pages)

Finally, we produce results that show the improvements made for the Tegola network. The best solution here would be to benchmark against existing max-flow formulations in the Cloud TE Tutorial, and produce some summary statistics that shadow those in chapter 3 to show how we have made improvements.
