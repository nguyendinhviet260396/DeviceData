import os
import sys
import time
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.constants import Defaults
Defaults.RetryOnEmpty = True
Defaults.Timeout = 5
Defaults.Retries = 5

"""
    #Function Code	Register Type
    # 1   Read Coil
    # 2   Read Discrete Input
    # 3   Read Holding Registers
    # 4	  Read Input Registers
    # 5	  Write Single Coil
    # 6	  Write Single Holding Register
    # 15  Write Multiple Coils
    # 16  Write Multiple Holding Registers
"""


class ModbusRTU:
    def __init__(self):
        # ls /dev (self.modbusRTU_port = '/dev/ttyUSB0')
        self.modbusRTU_port = ''
        self.modbusRTU_stopbits = 1
        self.modbusRTU_bytesize = 8
        self.modbusRTU_parity = 'N'
        self.modbusRTU_baudrate = 9600

    def connection_RTU(self):
        try:
            connection = ModbusSerialClient(
                method='rtu',
                port=self.modbusRTU_port,
                timeout=1,
                stopbits=self.modbusRTU_stopbits,
                bytesize=self.modbusRTU_bytesize,
                parity=self.modbusRTU_parity,
                baudrate=self.modbusRTU_baudrate)
            return connection
        except Exception as e:
            time.sleep(60)
            print(e)


class ModbusTCP:
    def __init__(self):
        self.modbusTCP_port = 502
        self.modbusTCP_host = '127.0.0.1'

    def connection_TCP(self):
        TCP_connection = ModbusTcpClient(
            host=self.modbusTCP_host,
            port=self.modbusTCP_port,
        )
        return TCP_connection
