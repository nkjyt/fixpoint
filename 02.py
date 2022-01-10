"""
2022/01/08 中島悠太
"""
import csv
from datetime import datetime as dt

#パラメータ
N = 3
errorRes = '-'
log = {}
file_name = 'log/server_observation_4.csv'

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


def timeout_check(log):
    for key in log.keys():
        startAt = None
        count = 0
        for x in log[key]:
            if x["response"] == errorRes:
                if startAt == None:
                    startAt = x["timestamp"]
                count += 1
            else:
                if count >= N:
                    print(f"{key} : {startAt} ~ {x['timestamp']}")
                count = 0
                startAt = None
        if count >= N:
            print(f"{key} : {startAt} ~")

log = load_file()
timeout_check(log)