#!/usr/bin/python3
import paho.mqtt.client as mqtt
import json
import configparser
import logging
from pprint import pprint,pformat
from datapoint import DataPoint

CONFIG_FILE = "input.conf"

config = configparser.ConfigParser()
config.read("input.conf")

BASE_TOPIC = config['mqtt']["base_topic"]
HOST = config['mqtt']['host']
LOGFILE = config['logging']['file']

logging.basicConfig(filename=LOGFILE,level=logging.DEBUG)

def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code "+str(rc))
    client.subscribe(BASE_TOPIC+'#')
    client.message_callback_add(BASE_TOPIC+'#',on_message)

def on_message(client, userdata, msg):
    logging.debug("Received "+msg.topic+" "+str(msg.payload))
    try:
        structured = json.loads(str(msg.payload,"utf8"))
        logging.debug("Decoded: "+pformat(structured))

        if "signature" in structured:
            logging.debug("Found signature: "+repr(structured["signature"]))
            #TODO: check signature
            del structured["signature"]
        elif "token" in structured:
            logging.debug("Found token: "+repr(structured["token"]))
            #TODO: check token
            del structured["token"]

        for key,value in structured.items():
            try:
                sensorid = key.split(".")[0]
                channel = key.split(".")[1]
                dp = DataPoint(sensorid=sensorid, channel=channel, value=value)

                logging.debug("Got data point: "+str(dp))
            except IndexError as e:
                logging.warning("Failed to extract channel: "+str(e))
        
    except json.JSONDecodeError as e:
        logging.warning("Error decoding payload: "+str(e))

client = mqtt.Client()
client.on_connect = on_connect

client.connect(HOST)

client.loop_forever()
