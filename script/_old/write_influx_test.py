#!/usr/bin/env python
from influxdb import InfluxDBClient
from datetime import datetime
import time
import random

# データベースに接続
# Before launch the script, create the DB as follows
# $ influx //launch the influxDB shell 
# $ >> CREATE DATABASE sample_Db
# $ >> exit
dbclient = InfluxDBClient(host='localhost', port=8086, database='sample_db')

while True:
    try:
        co1 = random.random()
        hr2 = random.random() 
        hr3 = random.random() 

        print("coil1: {0}, holding2: {1}, holding3: {2}".format(co1, hr2, hr3))

        # データベースへの書き込み
        json_body = [
            {
                "measurement": "sample_measurement",
                "time": datetime.utcnow(),
                "fields": {
                    "coil_1": co1,
                    "holding_register_2": hr2,
                    "holding_register_3": hr3
                }
            }
        ]
        print("Write points: {0}".format(json_body))
        dbclient.write_points(json_body)

        # 5秒スリープ
        time.sleep(5)

    except KeyboardInterrupt:
        dbclient.close()
        break
    
    except Exception as e:
        print(e)

