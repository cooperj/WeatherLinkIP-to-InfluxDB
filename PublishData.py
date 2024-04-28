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
# loop2 = Loop2Packet(data)
weatherlink_socket.close()

# Write data to InfluxDB
write_api = influxClient.write_api(write_options=SYNCHRONOUS)
p = influxdb_client.Point("weather") \
                    .tag("location", WEATHERLINK_SITENAME) \
                    .field("temperature_outside", float(loop.outside_temp)) \
                    .field("humidity_outside", float(loop.out_hum)) \
                    .field("wind_speed_kmh", float(loop.wind_speed)) \
                    .field('wind_direction', int(loop.wind_dir)) \
                    .field('wind_direction_average_10_minute', int(loop.ten_min_avg_wind_spd)) \
                    .field('forecast', loop.forecast_icons) \
                    .field('forecast_rule', loop.forecast_rule) \
                    .field('trend', loop.bar_trend) \
                    .field('humidity_inside', float(loop.inside_hum)) \
                    .field('temperature_inside', float(loop.inside_temp)) \
                    .field('barometer', float(loop.barometer)) \
                    .field('external_temperature_1', float(loop.ex_temp_1)) \
                    .field('external_temperature_2', float(loop.ex_temp_2)) \
                    .field('external_temperature_3', float(loop.ex_temp_3)) \
                    .field('external_temperature_4', float(loop.ex_temp_4)) \
                    .field('external_temperature_5', float(loop.ex_temp_5)) \
                    .field('external_temperature_6', float(loop.ex_temp_6)) \
                    .field('external_temperature_7', float(loop.ex_temp_7)) \
                    .field('soil_temperature_1', float(loop.soil_temp_1)) \
                    .field('soil_temperature_2', float(loop.soil_temp_2)) \
                    .field('soil_temperature_3', float(loop.soil_temp_3)) \
                    .field('soil_temperature_4', float(loop.soil_temp_4)) \
                    .field('leaf_temperature_1', float(loop.leaf_temp_1)) \
                    .field('leaf_temperature_2', float(loop.leaf_temp_2)) \
                    .field('leaf_temperature_3', float(loop.leaf_temp_3)) \
                    .field('leaf_temperature_4', float(loop.leaf_temp_4)) \
                    .field('external_humidity_1', float(loop.ex_hum_1)) \
                    .field('external_humidity_2', float(loop.ex_hum_2)) \
                    .field('external_humidity_3', float(loop.ex_hum_3)) \
                    .field('external_humidity_4', float(loop.ex_hum_4)) \
                    .field('external_humidity_5', float(loop.ex_hum_5)) \
                    .field('external_humidity_6', float(loop.ex_hum_6)) \
                    .field('external_humidity_7', float(loop.ex_hum_7)) \
                    .field('rain_rate', float(loop.rain_rate)) \
                    .field('uv', float(loop.uv)) \
                    .field('solar_radiation', loop.solar_radiation) \
                    .field('storm_rain', float(loop.storm_rain)) \
                    .field('storm_start_date', loop.storm_start_date) \
                    .field('daily_rain', float(loop.day_rain)) \
                    .field('monthly_rain', float(loop.month_rain)) \
                    .field('yearly_rain', float(loop.year_rain)) \
                    .field('daily_et', float(loop.day_et)) \
                    .field('monthly_et', float(loop.month_et)) \
                    .field('yearly_et', float(loop.year_et)) \
                    .field('soil_moisture_1', float(loop.soil_moisture_1)) \
                    .field('soil_moisture_2', float(loop.soil_moisture_2)) \
                    .field('soil_moisture_3', float(loop.soil_moisture_3)) \
                    .field('soil_moisture_4', float(loop.soil_moisture_4)) \
                    .field('leaf_wetness_1', float(loop.leaf_wetness_1)) \
                    .field('leaf_wetness_2', float(loop.leaf_wetness_2)) \
                    .field('leaf_wetness_3', float(loop.leaf_wetness_3)) \
                    .field('leaf_wetness_4', float(loop.leaf_wetness_4)) \
                    .field('inside_alarms', loop.inside_alarms) \
                    .field('rain_alarms', loop.rain_alarms) \
                    .field('outside_alarms_1', loop.outside_alarms_1) \
                    .field('outside_alarms_2', loop.outside_alarms_2) \
                    .field('extra_temperature_humidity_alarm_1', loop.extra_temp_hum_alarm_1) \
                    .field('extra_temperature_humidity_alarm_2', loop.extra_temp_hum_alarm_2) \
                    .field('extra_temperature_humidity_alarm_3', loop.extra_temp_hum_alarm_3) \
                    .field('extra_temperature_humidity_alarm_4', loop.extra_temp_hum_alarm_4) \
                    .field('extra_temperature_humidity_alarm_5', loop.extra_temp_hum_alarm_5) \
                    .field('extra_temperature_humidity_alarm_6', loop.extra_temp_hum_alarm_6) \
                    .field('extra_temperature_humidity_alarm_7', loop.extra_temp_hum_alarm_7) \
                    .field('extra_temperature_humidity_alarm_8', loop.extra_temp_hum_alarm_8) \
                    .field('soil_leaf_alarm_1', loop.soil_leaf_alarm_1) \
                    .field('soil_leaf_alarm_2', loop.soil_leaf_alarm_2) \
                    .field('soil_leaf_alarm_3', loop.soil_leaf_alarm_3) \
                    .field('soil_leaf_alarm_4', loop.soil_leaf_alarm_4) \
                    .field('battery_status', loop.xmtr_battery_status) \
                    .field('battery_volts', float(loop.console_battery_volts)) \
                    .field('sunrise', loop.sunrise) \
                    .field('sunset', loop.sunset) \
                    .field('lf', loop.lf) \
                    .field('cr', loop.cr) \
                    .field('crc', loop.crc)

write_api.write(bucket=bucket, org=org, record=p)
