#/usr/bin/sh 
roscore &
rosrun rosserial_python serial_node.py /dev/ttyACM0
