import requests
import ast
import pwinput
import sys
from pprint import pprint
import copy

# We define the ordering of our sites as:
# 1: MHI, 2: SMO, 3:LSGR, 4:BLO
# 5: COR, 6: CAMUS, 7: PHONE, 8: BCO
# 9: SSH, 10: USGR, 11: INT-MHI, 12: INT-SMO

# Note that USGR has no internal demand, and INT-MHI and INT-SMO act as our gateway to the internet

API_URL = "https://phonebox.tegola.org.uk/api_jsonrpc.php"
NUM_VALUES = 1        # Data is collected every 3 minutes


# Calculate the demands for each node in the graph
def calculate_demands(auth_token):
    print("\n--> Initializing")

    output_demands = [[0 for i in range(12)] for j in range(12)]

    # Router -> Internet IDs
    rti_ids = [["47072", "47073", "47068", "47061"], ["47707", "47722", "47711"], ["45623"], ["46494"], ["46640", "46641"], 
           ["46131"], ["52250", "44809", "44811", "48758", "48759", "48760", "48761"], 
           ["46367", "46359", "46362", "46365", "46366"], ["45626", "45625", "45639"]]

    # Internet -> Router IDs
    itr_ids = [["47123", "47124", "47119", "47112"], ["47851", "47866", "47855"], ["45791"], ["46539"], ["46682", "46683"], 
           ["46074"], ["44896", "44898", "48803", "48804", "48805", "48806", "52256"], 
           ["46404", "46407", "46410", "46411", "46412"], ["45794", "45793", "45807"]]

    print("--> Calculating demands")

    # Sum demands over each item and store in an array
    for i in range(9):
        rti_sum = 0
        itr_sum = 0
        total_sum = 0

        for id in rti_ids[i]:
            rti_sum += build_request(id, auth_token)
        
        for id in itr_ids[i]:
            itr_sum += build_request(id, auth_token)

        if (i == 0 or i == 3):
            output_demands[i][10] = rti_sum / 1000000
            output_demands[10][i] = itr_sum / 1000000
        else:
            output_demands[i][11] = rti_sum / 1000000
            output_demands[11][i] = itr_sum / 1000000

        total_sum += output_demands[i][10] + output_demands[i][11] + output_demands[10][i] + output_demands[11][i]

    #print("--> Current sum of demands in the network: " + str(total_sum) + " bits")

    return output_demands


# Build the request for a specific item ID and return the value in bits
def build_request(id, auth_token):
    data = {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": 3,
                "itemids": id,
                "sortfield": "clock",
                "sortorder": "DESC",
                "limit": NUM_VALUES
            },
            "auth": auth_token,
            "id": 1
        }

    req = requests.post(API_URL, json=data)
    return int(ast.literal_eval(req.text)["result"][0].get("value"))


# Generate the authentication token for login
def get_auth_token(username, password):
    result = ""

    # JSON login request
    try:
        data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": username,
            "password": password
        },
        "id": 1,
        "auth": None
        }
        req = requests.post(API_URL, json=data)
        result = req.json()["result"]
    except:
        print("Error - incorrect credentials. Please try again.")
        exit()

    print("Zabbix Credentials Accepted.")
    return result


# Perform arbitrary split on demand matrix. Naive implementation
def split(demand, split_proportion):
    updated_demands = [[0 for i in range(12)] for j in range(12)]

    # split_proportion goes in/out via Mhialairigh, (1 - split_proportion) goes in/out via SMO
    for i in range(9):
        if (demand[i][10] == 0):
            updated_demands[i][10] = split_proportion * demand[i][11]
            updated_demands[i][11] = (1 - split_proportion) * demand[i][11]
        else:
            updated_demands[i][10] = split_proportion * demand[i][10]
            updated_demands[i][11] = (1 - split_proportion) * demand[i][10]

        if (demand[10][i] == 0):
            updated_demands[10][i] = split_proportion * demand[11][i]
            updated_demands[11][i] = (1 - split_proportion) * demand[11][i]
        else:
            updated_demands[10][i] = split_proportion * demand[10][i]
            updated_demands[11][i] = (1 - split_proportion) * demand[10][i]

    return updated_demands


def split_improved(demand, split_proportion):
    updated_demands = copy.deepcopy(demand)
    total_demand_out = 0
    total_demand_in = 0

    for i in range(9):
        total_demand_out += demand[i][10] + demand[i][11]
        total_demand_in += demand[10][i] + demand[11][i]
    #print("total traffic: " + str(total_demand_in + total_demand_out))

    mhi_demand_out = total_demand_out * split_proportion
    mhi_demand_in = total_demand_in * split_proportion
    unused = [0,3,4,6,7,8,2,5,1]
    traffic_to_mhi_out = 0
    traffic_to_mhi_in = 0

    for node in unused:
        node_traffic_out = demand[node][10] + demand[node][11]
        node_traffic_in = demand[10][node] + demand[11][node]

        # Check if we will exceed MHI demand by adding full amount of traffic
        if (traffic_to_mhi_out + node_traffic_out > mhi_demand_out):
            traffic_through_node = mhi_demand_out - traffic_to_mhi_out

            # send as much traffic as possible through MHI, and the remainder through SMO
            updated_demands[node][10] = traffic_through_node
            updated_demands[node][11] = node_traffic_out - traffic_through_node
            traffic_to_mhi_out += traffic_through_node
        else:
            traffic_to_mhi_out += node_traffic_out

            # Send all the node traffic through MHI, and 0 through SMO
            updated_demands[node][10] = node_traffic_out
            updated_demands[node][11] = 0


        # Check if we will exceed MHI demand by adding full amount of traffic
        if (traffic_to_mhi_in + node_traffic_in > mhi_demand_in):
            traffic_through_node = mhi_demand_in - traffic_to_mhi_in

            # send as much traffic as possible through MHI, and the remainder through SMO
            updated_demands[10][node] = traffic_through_node
            updated_demands[11][node] = node_traffic_in - traffic_through_node
            traffic_to_mhi_in += traffic_through_node
        else:
            traffic_to_mhi_in += node_traffic_in

            # Send all the node traffic through MHI, and 0 through SMO
            updated_demands[10][node] = node_traffic_in
            updated_demands[11][node] = 0

    return updated_demands


# Main
if __name__ == "__main__":

    # Read user arguments
    valid_split = False
    split_proportion = 0

    if (len(sys.argv) == 2):
        valid_split = True
        split_proportion = float(sys.argv[1])

    username = input("\nEnter Zabbix Username: ")
    password = pwinput.pwinput("Enter Password: ")

    # Communicate with Zabbix API to read the demands
    auth_token = get_auth_token(username, password)
    demand = calculate_demands(auth_token)

    # Perform split if necessary
    if (split_proportion >= 0 and split_proportion <= 1 and valid_split):
        print("--> Valid split value detected, performing split with " + str(split_proportion * 100) 
        + "% of traffic routed through Mhialairigh")
        demand = split_improved(demand, split_proportion)
    else:
        print("--> No valid split value detected. Valid split values lie in the real number range (0,1). No split performed.")

    # Write to demand file
    print("--> Writing to file")
    file = open("demand.txt", "w")
    
    for i in range(12):
        for j in range(12):
            file.write(str(demand[i][j]) + " ")

    print("\nProcess complete.\n")
    print("Demands have been written to: demand.txt\n")

    pprint(demand)
    file.close()