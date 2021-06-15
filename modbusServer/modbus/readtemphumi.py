import time
import json
from datetime import datetime
from config.db import run, connection
from config.modbusConnect import ModbusRTU

ModbusRTU = ModbusRTU()
ModbusRTU.modbusRTU_port = 'COM4'
ModbusRTU = ModbusRTU.connection_RTU()
ModbusRTU.connect()


def readtemphumi(slave_unit):
    try:
        if ModbusRTU.connect():
            value = ModbusRTU.read_input_registers(
                address=1, count=2, unit=slave_unit)
            if not value.isError():
                name = "tempHumi_0"+str(slave_unit)
                print(name, ":", value.registers)
                return value.registers
            else:
                return []
        else:
            return []
    except Exception as e:
        return []

        print(e)


def readPmu(slave_unit):
    try:
        if ModbusRTU.connect():
            value = ModbusRTU.read_holding_registers(
                address=0, count=12, unit=slave_unit)
            if not value.isError():
                values = value.registers
                print("pmu", values)
                return values
            else:
                return []
        else:
            return []
    except Exception as e:
        return []

        print(e)
