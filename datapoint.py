#!/usr/bin/python3
import datetime

class DataPoint():
    def __init__(self, sensorid, channel, value, timestamp=None):
        self.sensorid = sensorid
        self.channel = channel
        self.value = value
        self.timestamp = timestamp
        if self.timestamp is None:
            self.timestamp = datetime.datetime.now(datetime.timezone.utc)

    def __str__(self):
        return str(self.sensorid)+"."+str(self.channel)+": "+str(self.value)+" @"+str(self.timestamp)
