"""
2022/01/08 中島悠太
"""
import csv
from datetime import datetime as dt

#パラメータ
m = 3
t = 512
N = 3
errorRes = '-'
log = {}
file_name = 'log/server_observation_6.csv'

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

#設問2：タイムアウトをチェックする関数
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

#設問3：過負荷をチェックする関数
def overload(log):
    for key in log.keys():
        li = []
        if len(log[key]) >= m:
            #try:
            for i in range(len(log[key])-1, len(log[key])-4, -1):
                try:
                    li.append(int(log[key][i]['response']))
                except:
                    print(f"{key}は直近{m}回のアクセスでタイムアウトしました．")
                    li = []
                    break
            if li != []: 
                average = sum(li)/ len(li)
                if average >= t:
                    print(f"{key} : {log[key][-m]['timestamp']} ~ {log[key][-1]['timestamp']}")

log = load_file()
overload(log)