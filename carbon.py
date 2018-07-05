#!/usr/bin/python3
import configparser
import logging
import time, datetime
import socketserver
from pprint import pprint,pformat
from datapoint import DataPoint
from database import DbConnection

CONFIG_FILE = "ingress.conf"

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

LOGFILE = config['logging']['file']
LISTEN = config['carbon']['listen']
PORT = config['carbon'].getint('port')

logging.basicConfig(filename=LOGFILE,
                    level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

db = DbConnection()

class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        line = str(self.rfile.readline().strip(),"utf8")
        logging.debug(line)
        fields = line.split()
        logging.debug(fields)
        sensorid,channel = fields[0].split(".")
        value = float(fields[1])
        timestamp = int(fields[2])
        dp = DataPoint(sensorid=sensorid,channel=channel,value=value,timestamp=datetime.datetime.fromtimestamp(timestamp,tz=datetime.timezone.utc))
        logging.debug(dp)

addr = (LISTEN,PORT)

server = socketserver.TCPServer(addr, RequestHandler)
server.serve_forever()
