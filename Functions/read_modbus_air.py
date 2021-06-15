import time
import json
from datetime import datetime
from Configs.db import run, connection
from Configs.modbus import ModbusRTU

ModbusRTU = ModbusRTU()
ModbusRTU.modbusRTU_port = 'COM2'
ModbusRTU = ModbusRTU.connection_RTU()
ModbusRTU.connect()
slave_id = 1

def readCoilAir():
    try:
        if ModbusRTU.connect():
            value = ModbusRTU.read_coils(address=0, count=16, unit=slave_id)
            if not value.isError():

                return value.bits
            else:
                create_data = []
                for i in range(0, 16):
                    create_data.append(None)
                return create_data
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
                return value.registers
            else:
                create_data = []
                for i in range(0, 24):
                    create_data.append(None)
                return create_data
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
                return value.registers
            else:
                create_data = []
                for i in range(0, 16):
                    create_data.append(None)
                return create_data
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
                return value.bits
            else:
                create_data = []
                for i in range(0, 34):
                    create_data.append(None)
                return create_data
        else:
            return []
    except Exception as e:
        return []
        print(e)


def readAir():
    try:
        values = []
        # coils
        value_coil = readCoilAir()
        values.extend(value_coil)
        # holding registers
        value_hold = readHoldingRegisterAir()
        values.extend(value_hold)
        # holding registers
        value_input = readInputRegisterAir()
        values.extend(value_input)
        # discrete input
        value_dis = readDiscreteInputs()
        values.extend(value_dis)
        if len(values):
            query = """
                INSERT INTO airtable(device_id,infanstatus01,infanstatus02,exfanstatus01,exfanstatus02,compstatus,heaterstatus,infanspeed01,infanspeed02,extfanspeed01,extfanspeed02,returntemp,retunhumi,ambienttemp,voldc,volac,compressorcurrent,heatercurrent,compressorspeed,compressorfre,dcpowercurrent,e01,e02,e03,e04,e05,e06,e07,e08,e09,e10,e11,e12,e13,e14,e15,e16,e17,e18,e19,e20,e21,e22,e23,e24,e26,e27,e28,e31,e32,e33,e34,timestamp)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            params = ('air', values[0], values[1], values[2], values[3], values[4], values[5], values[32], values[33], values[34], values[35], values[36], values[37], values[38], values[46], values[47], values[48], values[49], values[50], values[53], values[55], values[56], values[57], values[58], values[59], values[60], values[61], values[62],
                      values[63], values[64], values[65], values[66], values[67], values[68], values[69], values[70], values[71], values[72], values[73], values[74], values[75], values[76], values[77], values[78], values[79], values[81], values[82], values[83], values[86], values[87], values[88], values[89], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            run(query, params)
        print(values)
        return values

    except:
        print("connect  timeout ...!")


if __name__ == "__main__":
    while True:
        readAir()
        time.sleep(1)
