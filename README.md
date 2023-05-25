## Install InfluxDB (server and python client) and Grafana
$ sudo apt-get install influxdb2
$ pip3 install influxdb-client
$ sudo apt install grafana
## Launch InfluxDB (at :8086)
$ sudo  systemctl unmask influxdb
$ sudo  systemctl start influxdb
## Launch Grafana (at :3000)
$ sudo systemctl start grafana-server

