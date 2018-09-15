#!/usr/bin/python3
import paho.mqtt.client as mqtt
import json
import configparser
import logging
import time, datetime
from pprint import pprint,pformat
from datapoint import DataPoint
from database import DbConnection

CONFIG_FILE = "ingress.conf"

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

BASE_TOPIC = config['mqtt']["base_topic"]
HOST = config['mqtt']['host']
LOGFILE = config['logging']['file']

logging.basicConfig(filename=LOGFILE,
                    level=logging.DEBUG,
                    format="%(asctime)s MQTT %(levelname)s %(message)s")

db = DbConnection()

def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code "+str(rc))
    client.subscribe(BASE_TOPIC+'#')
    client.message_callback_add(BASE_TOPIC+'#',on_message)

def on_message(client, userdata, msg):
    logging.debug("Received "+msg.topic+" "+str(msg.payload))
    try:
        structured = json.loads(str(msg.payload,"utf8"))
        logging.debug("Decoded: "+pformat(structured))

        timestamp = time.time()

        if "signature" in structured:
            logging.debug("Found signature: "+repr(structured["signature"]))
            #TODO: check signature
            del structured["signature"]
        elif "token" in structured:
            logging.debug("Found token: "+repr(structured["token"]))
            #TODO: check token
            del structured["token"]
        
        if "timestamp_ms" in structured:
            timestamp = structured["timestamp_ms"]/1000
        elif "timestamp" in structured:
            timestamp = structured["timestamp"]

        for key,value in structured.items():
            try:
                sensorid = key.split(".")[0]
                if sensorid != "timestamp":
                  channel = key.split(".")[1]
                  dp = DataPoint(sensorid=sensorid, channel=channel, value=value, timestamp=datetime.datetime.fromtimestamp(timestamp,tz=datetime.timezone.utc))

                  logging.debug("Got data point: "+str(dp))

                  db.store_point(dp)
            except IndexError as e:
                logging.warning("Failed to extract channel: "+str(e))
        
    except json.JSONDecodeError as e:
        logging.warning("Error decoding payload: "+str(e))

client = mqtt.Client()
client.on_connect = on_connect

client.connect(HOST)

client.loop_forever()
