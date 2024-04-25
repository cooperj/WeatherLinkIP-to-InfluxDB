import os
import socket
from WeatherLink import *
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Get properties from the .env file
token = os.environ['INFLUXDB_TOKEN']
org = os.environ['INFLUXDB_ORG']
url = str(os.environ['INFLUXDB_URL'])

influxClient = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# WeatherLink configuration
WEATHERLINK_IP = os.environ['WEATHERLINK_IP']
WEATHERLINK_PORT = int(os.environ['WEATHERLINK_PORT'])
WEATHERLINK_SITENAME = os.environ['WEATHERLINK_SITENAME']
bucket = os.environ['INFLUXDB_BUCKET']

# Get data from weather station
weatherlink_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
weatherlink_socket.connect((WEATHERLINK_IP, WEATHERLINK_PORT))
weatherlink_socket.sendall(b"LOOP 1\n")
data = weatherlink_socket.recv(1024)
loop = LoopPacket(data)
weatherlink_socket.sendall(b"LPS 2 1\n")
data = weatherlink_socket.recv(1024)
loop2 = Loop2Packet(data)
weatherlink_socket.close()

# Write data to InfluxDB
write_api = influxClient.write_api(write_options=SYNCHRONOUS)
p = influxdb_client.Point("weather").tag("location", WEATHERLINK_SITENAME).field("temperature_outside", float(loop.outside_temp)).field("humidity_outside", float(loop.out_hum)).field("wind_speed_kmh", float(loop.wind_speed)).field('wind_direction', int(loop.wind_dir)).field('forecast', loop.forecast_icons).field('trend', loop.bar_trend).field('daily_rain', float(loop.day_rain)).field('humidity_inside', float(loop.inside_hum)).field('temperature_inside', float(loop.inside_temp)).field('barometer', float(loop.barometer))

write_api.write(bucket=bucket, org=org, record=p)
