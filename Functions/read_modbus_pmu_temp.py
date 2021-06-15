import time
import json
import ast
import random
import pandas as pd
from datetime import datetime
from datetime import datetime
from Configs.db import run, connection
from Configs.modbus import ModbusRTU

ModbusRTU = ModbusRTU()
ModbusRTU.modbusRTU_port = 'COM2'
ModbusRTU = ModbusRTU.connection_RTU()
ModbusRTU.connect()


def analyticRegister(a, b):
    if a >= 0 and b >= 0:
        value = ''.join(["0x", hex(a)[2:].zfill(4), hex(b)[2:].zfill(4)])
        value = ast.literal_eval(value)
        return value
    elif a < 0 and b < 0:
        value = ''.join(["0x", hex(abs(b))[2:].zfill(4)])
        value = ast.literal_eval(value)
        return a*value
    elif a >= 0 and b < 0:
        x = b + 65536
        value = ''.join(["0x", hex(a)[2:].zfill(4), hex(x)[2:].zfill(4)])
        value = ast.literal_eval(value)
        return value

# get data from database


def readPmu():
    try:
        values = {
            "device_id": "pmu",
        }
        if ModbusRTU.connect():
            value = ModbusRTU.read_holding_registers(
                address=0, count=12, unit=4)
            if not value.isError():
                values["enegry"] = round(
                    (analyticRegister(value.registers[1], value.registers[0]))*0.1, 3)
                values["voltage"] = round((value.registers[2])/100, 2)
                values["current"] = round(
                    (analyticRegister(value.registers[4], value.registers[3]))*0.0001, 3)
                values["activepower"] = round(
                    (analyticRegister(value.registers[6], value.registers[5]))*0.1, 3)
                values["frequency"] = round((value.registers[11])/100, 2)
            if len(values):
                query = """
                    INSERT INTO pmutable (device_id,status,frequency,voltage,
                    current,activepower,enegry,timestamp)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                    """
                params = (values["device_id"], bool(1), values["frequency"], values["voltage"],
                          values["current"], values["activepower"], values["enegry"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                run(query, params)
            return values

    except:
        print("connect  timeout ...!")

def read_temp():
    try:
        values = []
        if ModbusRTU.connect():
            for slave_unit in range(1, 4):
                value = ModbusRTU.read_input_registers(
                    address=0, count=2, unit=slave_unit)
                if not value.isError():
                    name = "tempHumi_0"+str(slave_unit)
                    values.extend(value.registers)
                    query = """
                    INSERT INTO temhumitable(device_id,slave_id,temp,humi,timestamp)
                    VALUES(%s,%s,%s,%s,%s)
                    """
                    params = (name, slave_unit, value.registers[0], value.registers[1], datetime.now(
                    ).strftime("%Y-%m-%d %H:%M:%S"))
                    run(query, params)
                    # if value.registers[0] >= 300:
                    #     query = """
                    #     INSERT INTO alarmtable(device,type,discription,timestamp)
                    #     VALUES(%s,%s,%s,%s)
                    #     """
                    #     params = (name, 'warring', 'Over Tempraturn: '+str(
                    #         value.registers[0]/10), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    #     run(query, params)
            return {
                "tempHumi": [
                    {"device_id": "tempHumi_01",
                        "temp": values[0],
                        "humi": values[1],
                     },
                    {"device_id": "tempHumi_02",
                        "temp": values[2],
                        "humi": values[3],
                     },
                    {"device_id": "tempHumi_03",
                        "temp": values[4],
                        "humi": values[5],
                     }
                ],
            }

    except:
        print("connect  timeout ...!")

if __name__ == "__main__":
    while True:
        readPmu()
        read_temp()
        time.sleep(1)
