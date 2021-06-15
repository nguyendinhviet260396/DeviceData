import os
import sys
import time
from pymodbus.client.sync import ModbusTcpClient


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
