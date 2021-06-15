import time
import json
from datetime import datetime
from config.db import run, connection
from config.modbusConnect import ModbusRTU

ModbusRTU = ModbusRTU()
ModbusRTU.modbusRTU_port = 'COM9'
ModbusRTU = ModbusRTU.connection_RTU()
ModbusRTU.connect()
slave_id = 6


def readCoilAir():
    try:
        if ModbusRTU.connect():
            value = ModbusRTU.read_coils(address=0, count=16, unit=slave_id)
            if not value.isError():
                print("Air", value.bits)
                return value.bits
            else:
                return []
        else:
            return []
    except Exception as e:
        return []
        print(e)


def readInputRegisterAir():
    try:
        if ModbusRTU.connect():
            value = ModbusRTU.read_input_registers(
                address=0, count=24, unit=slave_id)
            if not value.isError():
                print("Air", value.registers)
                return value.registers
            else:
                return []

        else:
            return []
    except Exception as e:
        return []
        print(e)


def readHoldingRegisterAir():
    try:
        if ModbusRTU.connect():
            value = ModbusRTU.read_holding_registers(
                address=0, count=16, unit=slave_id)
            if not value.isError():
                print("Air", value.registers)
                return value.registers
            else:
                return []
        else:
            return []
    except Exception as e:
        return []
        print(e)


def readDiscreteInputs():
    try:
        if ModbusRTU.connect():
            value = ModbusRTU.read_discrete_inputs(
                address=0, count=34, unit=slave_id)
            if not value.isError():
                print("Air", value.bits)
                return value.bits
            else:
                return []
        else:
            return []
    except Exception as e:
        return []
        print(e)
