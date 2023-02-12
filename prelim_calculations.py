import requests
import ast
import datetime
import time

# We define the ordering of our sites as:
# 1: MHI, 2: SMO, 3:LSGR, 4:BLO
# 5: COR, 6: CAMUS, 7: PHONE, 8: BCO
# 9: SSH, 10: USGR, 11: INT-MHI, 12: INT-SMO

# Note that USGR has no internal demand, and INT-MHI and INT-SMO act as our gateway to the internet

class Calculate:

    def __init__(self, start, end):
        self.API_URL = "https://phonebox.tegola.org.uk/api_jsonrpc.php"
        self.NUM_VALUES = 1        # Data is collected every 3 minutes
        self.username = "yeyao"
        self.password = "ci5WeJoh"

        self.start_date = int(time.mktime(start))
        self.end_date = int(time.mktime(end))

        # Router -> Internet IDs
        self.rti_ids = [["47072", "47073", "47068", "47061"], ["47707", "47722", "47711"], ["45623"], ["46494"], ["46640", "46641"], 
           ["46131"], ["52250", "44809", "44811", "48758", "48759", "48760", "48761"], 
           ["46367", "46359", "46362", "46365", "46366"], ["45626", "45625", "45639"]]

        # Internet -> Router IDs
        self.itr_ids = [["47123", "47124", "47119", "47112"], ["47851", "47866", "47855"], ["45791"], ["46539"], ["46682", "46683"], 
           ["46074"], ["44896", "44898", "48803", "48804", "48805", "48806", "52256"], 
           ["46404", "46407", "46410", "46411", "46412"], ["45794", "45793", "45807"]]

    # Build the request for a specific item ID and return the value in bits
    def build_request(self, id, auth_token, take_half):
        data = {
                "jsonrpc": "2.0",
                "method": "history.get",
                "params": {
                    "output": "extend",
                    "history": 3,
                    "itemids": id,
                    "sortfield": "clock",
                    "sortorder": "DESC",
                    "time_from": self.start_date,
                    "time_till": self.end_date
                },
                "auth": auth_token,
                "id": 1
            }

        req = requests.post(self.API_URL, json=data)
        values = {}

        # Generates a dictionary with {time : sum of demands pairs for 3-minute intervals}

        count = 0

        for item in ast.literal_eval(req.text)["result"]:

            if ((count % 2 == 0 or count % 3 == 0 or count % 5 == 0) and take_half):
                count += 1
                continue
        
            clock = item.get("clock")
            value = int(item.get("value"))

            if datetime.datetime.fromtimestamp(int(clock)) in values.keys():
                values[datetime.datetime.fromtimestamp(int(clock))] += value * 0.0000009537
            else:
                values[datetime.datetime.fromtimestamp(int(clock))] = value * 0.0000009537

            count += 1
            
        return values


    # Generate the authentication token for login
    def get_auth_token(self):
        result = ""

        # JSON login request
        try:
            data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.username,
                "password": self.password
            },
            "id": 1,
            "auth": None
            }
            req = requests.post(self.API_URL, json=data)
            result = req.json()["result"]
        except:
            print("Error - incorrect credentials. Please try again.")
            exit()

        print("Zabbix Credentials Accepted.")
        return result

    def get_demands(self):
        demands = []
        token = self.get_auth_token()

        for list in self.itr_ids:
            demands.append(self.build_request(list, token, True))

        return demands
