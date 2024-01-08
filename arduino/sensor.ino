#include <ros.h>
#include <std_msgs/String.h>

ros::NodeHandle nh;

std_msgs::String temp_msg;
std_msgs::String humid_msg;
std_msgs::String moist_msg;
std_msgs::String ph_msg;
std_msgs::String ec_msg;
char temp_char_array[10];
char humid_char_array[10];
char moist_char_array[10];
char ph_char_array[10];
char ec_char_array[10];
ros::Publisher temperature("temperature", &temp_msg);
ros::Publisher humidity("humidity", &humid_msg);
ros::Publisher soil_moisture("soil_moisture", &moist_msg);
ros::Publisher ph("ph", &ph_msg);
ros::Publisher ec("ec", &ec_msg);

void setup()
{
  nh.initNode();
  nh.advertise(temperature);
  nh.advertise(humidity);
  nh.advertise(soil_moisture);
  nh.advertise(ph);
  nh.advertise(ec);
}

void loop()
{
  dtostrf(random(10,30), 8, 6, temp_char_array);
  dtostrf(random(20,80), 8, 6, humid_char_array);
  dtostrf(random(20,80), 8, 6, moist_char_array);
  dtostrf(random(5,7), 8, 6, ph_char_array);
  dtostrf(random(20,100), 8, 6, ec_char_array);
  temp_msg.data = temp_char_array;
  humid_msg.data = humid_char_array;
  moist_msg.data = moist_char_array;
  ph_msg.data = ph_char_array;
  ec_msg.data = ec_char_array;

  temperature.publish( &temp_msg);
  humidity.publish( &humid_msg);
  soil_moisture.publish( &moist_msg);
  ph.publish( &ph_msg);
  ec.publish( &ec_msg);
  nh.spinOnce();
  delay(5000);
}

