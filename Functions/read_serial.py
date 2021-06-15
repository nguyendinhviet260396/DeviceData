import time
import json
import pandas as pd
# import RPi.GPIO as GPIO
from datetime import datetime
from config.db import run, connection
from config.mqtt import connect_mqtt

# #select type serial is BCM
# GPIO.setmode(GPIO.BCM)

# # setup chanel raspberry pi 4 mode B

# #Chanel IN
# GPIO.setup( 16 , GPIO.IN) # input door 1
# GPIO.setup( 17 , GPIO.IN) # input door 2
# GPIO.setup( 22 , GPIO.IN) # input Leak
# GPIO.setup( 27 , GPIO.IN) # input Smoke
# GPIO.setup( 23 , GPIO.IN) # input Fan 1
# GPIO.setup( 24 , GPIO.IN) # input Fan 2
# GPIO.setup( 25 , GPIO.IN) # input Fan 3

# #Chanel OUT
# GPIO.setup( 5 , GPIO.OUT) #Fan 1
# GPIO.setup( 6 , GPIO.OUT) #Fan 2
# GPIO.setup( 19, GPIO.OUT) #Fan 3
# GPIO.setup( 26, GPIO.OUT) #Siren
# GPIO.setup( 8 , GPIO.OUT) #Control front linght
# GPIO.setup( 7 , GPIO.OUT) #Control back linght

# #Chanel IN
"""
Handle data input/output serial

"""

# read serial fan status 23,24,25


def readStatusFan():
    try:
        values = []
        for i in range(23, 26):
            #status = GPIO.input(i)
            status = 1
            if status > -1:
                values.append(status)
        print(values)
        for i in range(1, 4):
            device_id = "fan_0"+str(i)
            query = """
            UPDATE fantable
            SET device_id = %s,
                status = %s,
                control = %s
            WHERE id = (SELECT MAX(id)  FROM fantable WHERE device_id = %s );
            """
            params = (device_id, bool(
                values[i-1]),  bool(values[i-1]), device_id)
            run(query, params)
        return {
            "fanstatus": [
                {"device_id": "fan_01",
                    "status": bool(values[0])
                 },
                {"device_id": "fan_02",
                    "status": bool(values[1])
                 },
                {"device_id": "fan_03",
                    "status": bool(values[2])
                 }
            ]
        }
    except Exception as e:
        return []
        print(e)


# read serial smoke sensor 27
def readSmoke():
    try:
        #status = GPIO.input(27)
        status = 1
        if status > -1:
            query = """
                INSERT INTO smoketable(device_id,status,timestamp)
                VALUES(%s,%s,%s)
                """
            params = ("smokeSensor", bool(
                status), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            run(query, params)
            return {
                "device_id": "smokeSensor",
                "status": bool(status)
            }
            return [status]
    except Exception as e:
        return []
        print(e)
# read Door 16,17


def readDoor():
    try:
        values = []
        for i in range(16, 18):
            #statusDoor = GPIO.input(pin)
            status = 1
            if status > -1:
                values.append(status)
        print(values)
        for i in range(1, 3):
            device_id = "door0"+str(i)
            query = """
            INSERT INTO doortable(device_id,status,timestamp)
            VALUES(%s,%s,%s)
            """
            params = (device_id, bool(values[i-1]),
                      datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            run(query, params)
        return {
            "doorstatus": [
                {"device_id": "door01",
                    "status": bool(values[0])
                 },
                {"device_id": "door02",
                    "status": bool(values[1])
                 }
            ]
        }
        return values
    except Exception as e:
        return []
        print(e)

# read Leak


def readLeak():
    try:
        #status = GPIO.input(17)
        status = 0
        if status > -1:
            query = """
            INSERT INTO leaktable(device_id,status,timestamp)
            VALUES(%s,%s,%s)
            """
            params = ("leak", bool(status), datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"))
            run(query, params)
            return {
                "device_id": "leak",
                "status": bool(status)
            }

    except Exception as e:
        return []
        print(e)
