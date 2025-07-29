#!/usr/bin/env python3
import configparser
import logging
import time

import messaging

from payload import Payload



# Config has the connection properties.
def getConfig():
    configParser = configparser.ConfigParser()
    configParser.read('config.ini')
    config = configParser['DEFAULT']
    return config


def sensorData(client, userdata, msg):
    jsonString = msg.payload.decode('utf-8')
    logging.info('Received json: ' + jsonString)
    payload = Payload.from_json(jsonString)
    logging.info('Received message: ' + str(payload))




def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('Start of main.')
    config = getConfig()

    sensorDataMessenger = messaging.Messaging(config, 'sensor/data', sensorData)
    sensorDataMessenger.loop_start()

    # Example of how to publish a message. You will have to add arguments to the constructor on the next line:
    payload = Payload()
    payloadJson = payload.to_json()

    while (True):
        deviceCommandMessenger.publish('device/command', payloadJson)
        time.sleep(1)

if __name__ == '__main__':
    main()

