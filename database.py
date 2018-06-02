#!/usr/bin/python3
from influxdb import InfluxDBClient
from datapoint import DataPoint
import configparser

CONFIG_FILE = "ingress.conf"

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

database = config["influxdb"]["database"]
host = config["influxdb"]["host"]

client = InfluxDBClient(database=database, host=host)

def _datapoint_to_influx(datapoint):
    data = {
        "measurement": datapoint.sensorid,
        "fields": {
            datapoint.channel: datapoint.value
        },
        "time": datapoint.timestamp.isoformat()
    }
    return data

class DbConnection():
    def __init__(self):
        self.client = InfluxDBClient(database="testing")

    def store_point(self,datapoint):
        self.client.write_points([_datapoint_to_influx(datapoint)])

