#!/usr/bin/python3
import paho.mqtt.client as mqtt
import json
import configparser

CONFIG_FILE = "input.conf"

config = configparser.ConfigParser()
config.read("input.conf")

BASE_TOPIC = config['mqtt']["base_topic"]
HOST = config['mqtt']['host']

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(BASE_TOPIC+'#')
    client.message_callback_add(BASE_TOPIC+'#',on_message)

def on_message(client, userdata, msg):
    print("Recieved",msg.topic,str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect

client.connect(HOST)

client.loop_forever()
