#!/usr/bin/python3
import paho.mqtt.client as mqtt
import json
import configparser
import logging
from pprint import pprint,pformat

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
    logging.debug("Recieved "+msg.topic+" "+str(msg.payload))
    try:
        structured = json.loads(str(msg.payload,"utf8"))
        logging.debug("Decoded: "+pformat(structured))
    except json.JSONDecodeError as e:
        logging.warning("Error decoding payload: "+str(e))

client = mqtt.Client()
client.on_connect = on_connect

client.connect(HOST)

client.loop_forever()
