"""
2022/01/08 中島悠太
pip install netaddr　が必須

故障期間については，1とは異なり，ログに残っている最後の時間が終端時間となる
"""
import csv
from netaddr import *
from datetime import datetime as dt

#パラメータ
N = 2
errorRes = '-'
log = {}
subnet_table = {}
file_name = 'log/server_observation_7.csv'

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
        return data, dt.strptime(d, '%Y%m%d%H%M%S')


def get_subnet(IP):
    return str(IPNetwork(IP).network)

def make_subnet(log):
    table = {}
    for key in log.keys():
        subnet = get_subnet(key)
        try:
            table[subnet].append(key)
        except:
            table[subnet] = [key]
    return table

#02.pyの修正版
def timeout_check_key(log, keys):
    result = {}
    for key in keys:
        startAt = None
        count = 0
        for x in log[key]:
            if x["response"] == errorRes:
                if startAt == None:
                    startAt = x["timestamp"]
                count += 1
            else:
                if count >= N:
                    result[key] = {"start" : dt.strptime(startAt, '%Y%m%d%H%M%S'), "end" : dt.strptime(x['timestamp'], '%Y%m%d%H%M%S')}
                count = 0
                startAt = None
        if count >= N:
            result[key] = {"start" : dt.strptime(startAt, '%Y%m%d%H%M%S'), 'end' : None}
    return result

def check_subnet_error(subnet_table, log, finish_time):
    for subnet in subnet_table.keys():
        result = timeout_check_key(log, subnet_table[subnet])
        if len(result) >= len(subnet_table[subnet]):
            #被りの処理
            overlay_count = 1
            overlay_start, overlay_end = None, None
            for key in result.keys():
                if overlay_start == None:
                    overlay_start, overlay_end = result[key]['start'], result[key]['end']
                    if overlay_end is None: overlay_end = finish_time
                    continue
                time_start, time_end = result[key]['start'], result[key]['end']
                if time_end is None: time_end = finish_time
                if overlay_start < time_end or time_start < overlay_end:
                    overlay_count += 1
                    overlay_start = time_start if overlay_start < time_start else overlay_start
                    overlay_end = time_end if time_end < overlay_end else overlay_end
            if overlay_count == len(subnet_table[subnet]):
                print(f"{subnet}: {overlay_start} ~ {overlay_end}")


log, finish_time = load_file()
subnet_table = make_subnet(log)
check_subnet_error(subnet_table, log, finish_time)