#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def callback_temp(data):
    rospy.loginfo(rospy.get_caller_id() + "Temperature value:%s", data.data)
    
def callback_humid(data):
    rospy.loginfo(rospy.get_caller_id() + "Humidity value:%s", data.data)

def callback_moist(data):
    rospy.loginfo(rospy.get_caller_id() + "Soil moisture:%s", data.data)

def callback_ph(data):
    rospy.loginfo(rospy.get_caller_id() + "PH value:%s", data.data)

def callback_ec(data):
    rospy.loginfo(rospy.get_caller_id() + "EC value:%s", data.data)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("temperature", String, callback_temp)
    rospy.Subscriber("humidity", String, callback_humid)
    rospy.Subscriber("soil_moisture", String, callback_moist)
    rospy.Subscriber("ph", String, callback_ph)
    rospy.Subscriber("ec", String, callback_ec)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()

