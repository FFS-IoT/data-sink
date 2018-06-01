#!/usr/bin/python3

class DataPoint():
    def __init__(self, sensorid, channel, value):
        self.sensorid = sensorid
        self.channel = channel
        self.value = value

    def __str__(self):
        return str(self.sensorid)+"."+str(self.channel)+": "+str(self.value)
