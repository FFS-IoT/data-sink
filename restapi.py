import logging
import configparser
from datapoint import DataPoint
from flask import Flask, request
app = Flask(__name__)

CONFIG_FILE = "input.conf"

config = configparser.ConfigParser()
config.read("input.conf")

LOGFILE = config['logging']['file']

logging.basicConfig(filename=LOGFILE,
                    level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/input", methods=['GET', 'POST'])
def input_get():
    parameters = request.values.to_dict()

    logging.debug("Got request")
    token = parameters.get("token", None)
    signature = parameters.get("signature", None)

    if "signature" in parameters:
        logging.debug("Found signature: "+repr(parameters["signature"]))
        #TODO:check signature
        del parameters["signature"]
    elif "token" in parameters:
        logging.debug("Found token: "+repr(parameters["token"]))
        #TODO: check token
        del parameters["token"]

    for key,value in parameters.items():
        try:
            sensorid = key.split(".")[0]
            channel = key.split(".")[1]
            dp = DataPoint(sensorid=sensorid, channel=channel, value=value)

            logging.debug("Got data point: "+str(dp))
        except IndexError as e:
            logging.warning("Failed to extract channel: "+str(e))
    
    return "ok"
