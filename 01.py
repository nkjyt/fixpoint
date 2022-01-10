"""
2022/01/08 中島悠太
"""
import csv

errorRes = '-'
log = {}
file_name = 'log/server_observation_2.csv'

def load_file():
    data = {}
    with open(file_name) as f:
        reader = csv.reader(f)
        for row in reader:
            d, address, res = row[0], row[1], row[2]
            try:
                data[address].append({"timestamp" : d, "response" : res})
            except:
                data[address] = [{"timestamp" : d, "response" : res}]
        return data

log = load_file()

for key in log.keys():
    isTimeout = False
    startAt = None
    for x in log[key]:
        if x["response"] == errorRes:
            isTimeout = True
            if startAt is None:
                startAt = x["timestamp"]
        else:
            if isTimeout:
                print(f"{key} : {startAt} ~ {x['timestamp']}")
                isTimeout = False
                startAt = None
    if isTimeout:
        print(f"{key} : {startAt} ~")
