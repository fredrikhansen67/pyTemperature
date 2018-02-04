import glob
import time
import os
import pymongo

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'



def conn():
    result = read_temp()
    print(result[0])
    from pymongo import MongoClient
    dbcon = MongoClient("mongodb://192.168.1.33:27017/TEMPERATURES")
    db = dbcon.get_database()
    from datetime import datetime
    datum = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.temp.insert_one({"time": datum, "sensor": "1", "temp": result[0]}).inserted_id
    dbcon.close()


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return "%.2f" % temp_c, "%.2f" % temp_f


while True:
    conn()
    time.sleep(15)
