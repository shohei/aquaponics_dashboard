#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from influxdb import InfluxDBClient
from datetime import datetime
import time
import random

class Server():
    def __init__(self):
        # データベースに接続
        # Before launch the script, create the DB as follows
        # $ influx //launch the influxDB shell 
        # $ >> CREATE DATABASE aquaponicsDB
        # $ >> exit
        self.dbclient = InfluxDBClient(host='localhost', port=8086, database='aquaponicsDB')
        
        self.temp = 0
        self.humid = 0
        self.moist = 0
        self.ph = 0
        self.ec = 0

        rospy.init_node('listener', anonymous=True)
    
        rospy.Subscriber("temperature", String, self.callback_temp)
        rospy.Subscriber("humidity", String, self.callback_humid)
        rospy.Subscriber("moisture", String, self.callback_moist)
        rospy.Subscriber("ph", String, self.callback_ph)
        rospy.Subscriber("ec", String, self.callback_ec)
    
        rospy.spin()

    def callback_temp(self,data):
        #rospy.loginfo(rospy.get_caller_id() + "Temperature value:%s", data.data)
        self.temp = float(data.data)
        
    def callback_humid(self,data):
        #rospy.loginfo(rospy.get_caller_id() + "Humidity value:%s", data.data)
        self.humid = float(data.data)
    
    def callback_moist(self,data):
        rospy.loginfo(rospy.get_caller_id() + "Soil moisture:%s", data.data)
        self.moist = float(data.data)
    
    def callback_ph(self,data):
        #rospy.loginfo(rospy.get_caller_id() + "PH value:%s", data.data)
        self.ph = float(data.data)
    
    def callback_ec(self,data):
        #rospy.loginfo(rospy.get_caller_id() + "EC value:%s", data.data)
        self.ec = float(data.data)
        self.write_to_DB()
    
    def write_to_DB(self):
        print("temp: {0}, humid: {1}, moist: {2}, ph: {3}, ec: {4}".format(self.temp, self.humid, self.moist, self.ph, self.ec))
        try:
            # データベースへの書き込み
            json_body = [
                {
                    "measurement": "aquaponics_measurement",
                    "time": datetime.utcnow(),
                    "fields": {
                        "temp": self.temp,
                        "humid": self.humid,
                        "moist": self.moist,
                        "ph":self.ph,
                        "ec":self.ec
                    }
                }
            ]
            print("Write points: {0}".format(json_body))
            self.dbclient.write_points(json_body)
    
            # 5秒スリープ
            # time.sleep(5)
    
        except KeyboardInterrupt:
            dbclient.close()
            exit()
        
        except Exception as e:
            print(e)
    

if __name__ == '__main__':
    s = Server()

