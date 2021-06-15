
#!/usr/bin/env python
"""
Pymodbus Server With Updating Thread

"""
# --------------------------------------------------------------------------- #
# import the modbus libraries we need
# --------------------------------------------------------------------------- #
import time
from datetime import datetime
from modbus.readtemphumi import readtemphumi, readPmu
from modbus.readserial import readStatusFan, readSmoke, readLeak, readDoor
from modbus.readAir import readCoilAir, readDiscreteInputs, readHoldingRegisterAir, readInputRegisterAir
from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer
# -------------------------------------------------------------------------- #
# import the thread
# --------------------------------------------------------------------------- #
from threading import Thread

# --------------------------------------------------------------------------- #
# define your callback process
# --------------------------------------------------------------------------- #


def updating_writer_01(a):
    """ A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.
    :param arguments: The input arguments to the call
    """
    try:
        while True:
            function = 3
            address = 0x00
            for i in range(1, 5):
                context = a[i]
                if i < 4:
                    values = readtemphumi(i)
                    context.setValues(function, address, values)
                if i == 4:
                    values = readPmu(i)
                    context.setValues(function, address, values)
            # Fan status
            context = a[10]
            values_10 = readStatusFan()
            context.setValues(function, address, values_10)
            # Door status
            context = a[11]
            values_11 = readDoor()
            context.setValues(function, address, values_11)
            # Water Leak Status
            context = a[12]
            values_12 = readLeak()
            context.setValues(function, address, values_12)
            # Smoke status
            context = a[13]
            values_13 = readSmoke()
            context.setValues(function, address, values_13)
            # time.sleep(0.5)
    except Exception as e:
        print(e)


def updating_writer_02(a):
    """ 
    convert modbus RTU to TCP/IP
    """
    try:
        while True:
            context = a[6]
            # coils
            value_coil = readCoilAir()
            context.setValues(1, 0, value_coil)
            # discrete input
            value_dis = readDiscreteInputs()
            context.setValues(2, 0, value_dis)
            # holding registers
            value_hold = readHoldingRegisterAir()
            context.setValues(3, 0, value_hold)
            # input registers
            value_input = readInputRegisterAir()
            context.setValues(4, 0, value_input)
    except Exception as e:
        print(e)


def run_server():
    # ----------------------------------------------------------------------- #
    # initialize your data store
    # create registers data
    # ----------------------------------------------------------------------- #
    try:
        slaves = {}
        for id in range(1, 14):
            slaves[id] = ModbusSlaveContext(
                di=ModbusSequentialDataBlock(0, [0]*100),
                co=ModbusSequentialDataBlock(0, [0]*100),
                hr=ModbusSequentialDataBlock(0, [0]*100),
                ir=ModbusSequentialDataBlock(0, [0]*100))
        context = ModbusServerContext(slaves=slaves, single=False)

        # ----------------------------------------------------------------------- #
        # initialize the server information
        # ----------------------------------------------------------------------- #
        identity = ModbusDeviceIdentification()
        identity.VendorName = 'pymodbus'
        identity.ProductCode = 'PM'
        identity.VendorUrl = 'http://github.com/bashwork/pymodbus/'
        identity.ProductName = 'pymodbus Server'
        identity.ModelName = 'pymodbus Server'
        identity.MajorMinorRevision = '2.3.0'

        # ----------------------------------------------------------------------- #
        # run the server
        # ----------------------------------------------------------------------- #

        thread_01 = Thread(target=updating_writer_01, args=(context,))
        thread_02 = Thread(target=updating_writer_02, args=(context,))
        thread_01.start()
        thread_02.start()
        server = StartTcpServer(
            context, identity=identity, address=("0.0.0.0", 502))
        server.start()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    run_server()
