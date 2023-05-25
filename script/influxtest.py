import influxdb_client, os, time
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point, WritePrecision
import random

bucket = "test-bucket"

token = os.environ.get("INFLUXDB_TOKEN")
org = "shohei"
url = "http://192.168.1.222:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

write_api = client.write_api(write_options=SYNCHRONOUS)
   
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", int(random.random()*100))
  )
  write_api.write(bucket=bucket, org="shohei", record=point)
  time.sleep(1) # separate points by 1 second

query_api = client.query_api()

query = """from(bucket: "test-bucket")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "measurement1")
  |> mean()"""
tables = query_api.query(query, org="shohei")

for table in tables:
    for record in table.records:
        print(record)


