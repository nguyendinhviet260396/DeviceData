import time
import json
import pandas as pd
import RPi.GPIO as GPIO
from datetime import datetime
from config.db import run, connection

# select type serial is BCM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# setup chanel raspberry pi 4 mode B
# Chanel OUT
GPIO.setup(5, GPIO.OUT)  # Fan 1
GPIO.setup(6, GPIO.OUT)  # Fan 2
GPIO.setup(19, GPIO.OUT)  # Fan 3
GPIO.setup(7, GPIO.OUT)  # Siren
GPIO.setup(8, GPIO.OUT)  # Control front linght
GPIO.setup(26, GPIO.OUT)  # Control back linght

# Chanel IN
"""
Handle data input/output serial

"""


def controlFan_01():
    try:
        query = """
                SELECT device_id,status,control
                FROM fantable
                WHERE device_id ='fan_01'
                ORDER BY id DESC LIMIT 1
                """
        df = pd.read_sql(query, con=connection)
        if len(df) > 0:
            df = df.to_dict(orient='records')
            if df[0]['control'] == True:
                print("Turn On Fan 01")
                GPIO.output(5, GPIO.HIGH)
            else:
                print("Turn Off Fan 01")
                GPIO.output(5, GPIO.LOW)
    except Exception as e:
        print(e)


def controlFan_02():
    try:
        query = """
                SELECT device_id,status,control
                FROM fantable
                WHERE device_id ='fan_02'
                ORDER BY id DESC LIMIT 1
                """
        df = pd.read_sql(query, con=connection)
        if len(df) > 0:
            df = df.to_dict(orient='records')
            if df[0]['control'] == True:
                print("Turn On Fan 02")
                GPIO.output(6, GPIO.HIGH)
            else:
                print("Turn Off Fan 02")
                GPIO.output(6, GPIO.LOW)
    except Exception as e:
        print(e)


def controlFan_03():
    try:
        query = """
                SELECT device_id,status,control
                FROM fantable
                WHERE device_id ='fan_03'
                ORDER BY id DESC LIMIT 1
                """
        df = pd.read_sql(query, con=connection)
        if len(df) > 0:
            df = df.to_dict(orient='records')
            if df[0]['control'] == True:
                print("Turn On  Fan 03")
                GPIO.output(19, GPIO.HIGH)
            else:
                print("Turn Off Fan 03")
                GPIO.output(19, GPIO.LOW)
    except Exception as e:
        print(e)
# control light 01


def control_Light_01():
    try:
        query = """
                SELECT device_id,status
                FROM doortable
                WHERE device_id ='door01'
                ORDER BY id DESC LIMIT 1
                """
        df = pd.read_sql(query, con=connection)
        if len(df) > 0:
            df = df.to_dict(orient='records')
            if df[0]['status'] == True:
                print("Turn On Light 1")
                GPIO.output(8, GPIO.HIGH)
            else:
                print("Turn Off Light 1")
                GPIO.output(8, GPIO.LOW)
    except Exception as e:
        print(e)

# control light 02


def control_Light_02():
    try:
        query = """
                SELECT device_id,status
                FROM doortable
                WHERE device_id ='door02'
                ORDER BY id DESC LIMIT 1
                """
        df = pd.read_sql(query, con=connection)
        if len(df) > 0:
            df = df.to_dict(orient='records')
            if df[0]['status'] == True:
                print("Turn On Light 2")
                GPIO.output(26, GPIO.HIGH)
            else:
                print("Turn Off Light 2")
                GPIO.output(26, GPIO.LOW)
    except Exception as e:
        print(e)


def control_Fan_Follow():
    try:
        query = """
            SELECT  temp, humi
            FROM temhumitable
            WHERE slave_id= 2
            ORDER BY id DESC LIMIT 1
            """
        df_env = pd.read_sql(query, con=connection)
        df_env = df_env.div(10)
        if len(df_env) > 0:
            df_env = df_env.to_dict(orient='records')
            df_fan = []
            for device_id in ['fan_01', 'fan_02', 'fan_03']:
                query = """
                    SELECT device_id,status,control
                    FROM fantable
                    WHERE device_id ='%s'
                    ORDER BY id DESC LIMIT 1
                    """ % (device_id)
                df = pd.read_sql(query, con=connection)
                df = df.to_dict(orient='records')
                df_fan.extend(df)
            if df_env[0]['temp'] >= 25 and 70 >= df_env[0]['humi']:
                if df_fan[0]['status'] or df_fan[1]['status'] or df_fan[2]['status']:
                    if df_fan[0]['status'] and df_fan[1]['status'] or df_fan[1]['status'] and df_fan[2]['status'] or df_fan[2]['status'] and df_fan[0]['status']:
                        if df_fan[0]['status'] and df_fan[1]['status']:
                            print("Turn On Fan 01")
                            GPIO.output(5, GPIO.HIGH)
                            GPIO.output(6, GPIO.LOW)
                            GPIO.output(29, GPIO.LOW)
                        elif df_fan[1]['status'] and df_fan[2]['status']:
                            print("Turn On Fan 02")
                            GPIO.output(5, GPIO.LOW)
                            GPIO.output(6, GPIO.HIGH)
                            GPIO.output(29, GPIO.LOW)
                        else:
                            print("Turn On Fan 03")
                            GPIO.output(5, GPIO.LOW)
                            GPIO.output(6, GPIO.LOW)
                            GPIO.output(29, GPIO.HIGH)
                    elif df_fan[0]['status'] and df_fan[1]['status'] and df_fan[2]['status']:
                        print("Turn On Fan 01")
                        GPIO.output(5, GPIO.HIGH)
                        GPIO.output(6, GPIO.LOW)
                        GPIO.output(29, GPIO.LOW)
                    else:
                        print("Fan level I had turn on")

                else:
                    print("Turn On Fan 01")
                    GPIO.output(5, GPIO.HIGH)
                    GPIO.output(6, GPIO.LOW)
                    GPIO.output(29, GPIO.LOW)
            elif df_env[0]['temp'] >= 30 and 50 >= df_env[0]['humi']:
                if df_fan[0]['status'] and df_fan[1]['status'] or df_fan[1]['status'] and df_fan[2]['status'] or df_fan[2]['status'] and df_fan[0]['status']:
                    if df_fan[0]['status'] and df_fan[1]['status'] and df_fan[2]['status']:
                        print("Turn On Fan 01")
                        print("Turn On Fan 02")
                        GPIO.output(5, GPIO.HIGH)
                        GPIO.output(6, GPIO.HIGH)
                        GPIO.output(29, GPIO.LOW)
                    else:
                        print("Fan level II had turn on")
                else:
                    print("Turn On Fan 01")
                    print("Turn On Fan 02")
                    GPIO.output(5, GPIO.HIGH)
                    GPIO.output(6, GPIO.HIGH)
                    GPIO.output(29, GPIO.LOW)
            elif df_env[0]['temp'] >= 35 and 40 >= df_env[0]['humi']:
                if df_fan[0]['status'] and df_fan[1]['status'] and df_fan[2]['status']:
                    print("Fan level III had turn on")
                else:
                    print("Turn On Fan 01")
                    print("Turn On Fan 02")
                    print("Turn On Fan 03")
                    GPIO.output(5, GPIO.HIGH)
                    GPIO.output(6, GPIO.HIGH)
                    GPIO.output(29, GPIO.HIGH)
            else:
                controlFan_01()
                controlFan_02()
                controlFan_03()
        else:
            controlFan_01()
            controlFan_02()
            controlFan_03()

    except Exception as e:
        print(e)


def controlSiren():
    try:
        df_siren = []
        for device in ["ups", "pmu", "pdu", "air", "door1", "door2", "smoke", "leak", "temphumi1", "temphumi2", "temphumi3"]:
            query = """
                    SELECT type,device
                    FROM alarmtable
                     WHERE device ='%s' AND type='alarm'
                    ORDER BY id DESC LIMIT 1
                    """ % (device)
            df = pd.read_sql(query, con=connection)
            df = df.to_dict(orient='records')
            df_siren.extend(df)
        if len(df_siren) > 0:
            print("Turn On Siren")
            GPIO.output(7, GPIO.HIGH)
        else:
            print("Turn Off Siren")
            GPIO.output(7, GPIO.LOW)
    except Exception as e:
        print(e)


def run():
    start = time.time()
    control_Fan_Follow()
    controlSiren()
    control_Light_01()
    control_Light_02()
    stop = time.time()
    print("handle cycle:", stop-start)


if __name__ == "__main__":
    while connection:
        run()
        time.sleep(1)
