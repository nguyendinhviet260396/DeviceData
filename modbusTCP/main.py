import time
import json
import ast
import random
import pandas as pd
from datetime import datetime
from threading import Thread
from config.db import run, connection
# from config.mqtt import connect_mqtt,infor_mqtt
from config.modbus import ModbusTCP
from config.snmp import get, get_bulk, get_bulk_auto

# config modbus TCP
ModbusTCP = ModbusTCP()
ModbusTCP.modbusTCP_host = '127.0.0.1'
ModbusTCP = ModbusTCP.connection_TCP()
ModbusTCP.connect()


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


def read_ups():
    try:
        values = []
        if ModbusTCP.connect():
            value = ModbusTCP.read_holding_registers(
                address=0, count=42, unit=7)
            if not value.isError():
                values = value.registers
            if len(values) > 0:
                query = """
                INSERT INTO upstable (device_id,status,batstate,batcapacity,nomibatvolt,batvoltage,internaltemp,infrequency,involtage,outfrequency,outvoltage,outpower,
                failcounter,batterybad,batteryon,batterylow,batterydepleted,overtemp,inbad,outbad,outoverload,onbypass,bypassbad,outoffasreq,upsoffasreq,chargerfailed,
                upsoutoff,upssysoff,fanfail,fusefail,generalfault,comnlost,shutimminent,timestamp)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
                params = ("Ups", values[12], bool(1), values[6], values[11], values[13], values[10], values[14], values[7], values[14], values[0], values[3], values[17], bool(values[18]),
                          bool(values[19]), bool(values[20]), bool(values[21]), bool(values[22]), bool(values[23]), bool(
                              values[24]), bool(values[25]), bool(values[26]), bool(values[27]), bool(values[28]),
                          bool(values[29]), bool(values[30]), bool(values[31]), bool(values[32]), bool(values[33]), bool(values[34]), bool(values[35]), bool(values[37]), bool(values[40]), datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
                run(query, params)
                return {
                    "device_id": "Ups",
                    "status": values[12],
                    "batstate ": bool(1),
                    "batcapacity ": values[6],
                    "nomibatvolt ": values[11],
                    "batvoltage ": values[13],
                    "internaltemp ": values[10],
                    "infrequency ": values[14],
                    "involtage ": values[7],
                    "outfrequency ": values[14],
                    "outvoltage ": values[0],
                    "outpower ": values[3],
                    "failcounter ": values[17],
                    "batterybad ": bool(values[18]),
                    "batteryon ": bool(values[19]),
                    "batterylow ": bool(values[20]),
                    "batterydepleted ": bool(values[21]),
                    "overtemp ": bool(values[22]),
                    "inbad ": bool(values[23]),
                    "outbad ": bool(values[24]),
                    "outoverload ": bool(values[25]),
                    "onbypass ": bool(values[26]),
                    "bypassbad ": bool(values[27]),
                    "outoffasreq ": bool(values[28]),
                    "upsoffasreq ": bool(values[29]),
                    "chargerfailed ": bool(values[30]),
                    "upsoutoff ": bool(values[31]),
                    "upssysoff ": bool(values[32]),
                    "fanfail ": bool(values[33]),
                    "fusefail ": bool(values[34]),
                    "generalfault ": bool(values[35]),
                    "comnlost ": bool(values[37]),
                    "shutimminent ": bool(values[40]),
                }
    except:
        print("connect  timeout ...!")


def read_temp():
    try:
        values = []
        if ModbusTCP.connect():
            for slave_unit in range(1, 4):
                value = ModbusTCP.read_holding_registers(
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
                    if value.registers[0] >= 300:
                        query = """
                        INSERT INTO alarmtable(device,type,discription,timestamp)
                        VALUES(%s,%s,%s,%s)
                        """
                        params = (name, 'warring', 'Over Tempraturn: '+str(
                            value.registers[0]/10), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        run(query, params)

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


def readPmu():
    try:
        values = {
            "device_id": "pmu",
        }
        if ModbusTCP.connect():
            value = ModbusTCP.read_holding_registers(
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


def readSmoke():
    try:
        if ModbusTCP.connect():
            value = ModbusTCP.read_holding_registers(
                address=0, count=1, unit=13)
            if not value.isError():
                query = """
                INSERT INTO smoketable(device_id,status,timestamp)
                VALUES(%s,%s,%s)
                """
                params = ("smokeSensor", bool(
                    value.registers[0]), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                run(query, params)
                return {
                    "device_id": "smokeSensor",
                    "status": bool(value.registers[0])
                }
    except:
        print("connect  timeout ...!")

def readLeak():
    try:
        if ModbusTCP.connect():
            value = ModbusTCP.read_holding_registers(
                address=0, count=1, unit=12)
            if not value.isError():
                query = """
                INSERT INTO leaktable(device_id,status,timestamp)
                VALUES(%s,%s,%s)
                """
                params = ("leak", bool(value.registers[0]), datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"))
                run(query, params)
                return {
                    "device_id": "leak",
                    "status": bool(value.registers[0])
                }
    except:
        print("connect  timeout ...!")


def readDoor():
    try:
        if ModbusTCP.connect():
            value = ModbusTCP.read_holding_registers(
                address=0, count=2, unit=11)
            if not value.isError():
                for i in range(1, 3):
                    device_id = "door0"+str(i)
                    query = """
                    INSERT INTO doortable(device_id,status,timestamp)
                    VALUES(%s,%s,%s)
                    """
                    params = (device_id, bool(value.registers[i-1]),
                              datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    run(query, params)
                return {
                    "doorstatus": [
                        {"device_id": "door01",
                         "status": bool(value.registers[0])
                         },
                        {"device_id": "door02",
                         "status": bool(value.registers[1])
                         }
                    ]
                }
    except:
        print("connect  timeout ...!")


def readStatusFan():
    try:
        if ModbusTCP.connect():
            value = ModbusTCP.read_holding_registers(
                address=0, count=3, unit=10)
            if not value.isError():
                # for i in range(1, 4):
                #     device_id = "fan_0"+str(i)
                #     query = """
                #     UPDATE fantable
                #     SET device_id = %s,
                #         status = %s,
                #         control = %s
                #     WHERE id = (SELECT MAX(id)  FROM fantable WHERE device_id = %s );
                #     """
                #     params = (device_id, bool(
                #         value.registers[i-1]),  bool(value.registers[i-1]), device_id)
                #     run(query, params)
                return {
                    "fanstatus": [
                        {"device_id": "fan_01",
                         "status": bool(value.registers[0])
                         },
                        {"device_id": "fan_02",
                         "status": bool(value.registers[1])
                         },
                        {"device_id": "fan_03",
                         "status": bool(value.registers[2])
                         }
                    ]
                }
    except:
        print("connect  timeout ...!")


def readAir():
    try:
        values = []
        if ModbusTCP.connect():
            value = ModbusTCP.read_coils(
                address=0, count=16, unit=6)
            if not value.isError():
                values.extend(value.bits)
            value = ModbusTCP.read_holding_registers(
                address=0, count=16, unit=6)
            if not value.isError():
                values.extend(value.registers)
            value = ModbusTCP.read_input_registers(
                address=0, count=24, unit=6)
            if not value.isError():
                values.extend(value.registers)
            value = ModbusTCP.read_discrete_inputs(address=0, count=34, unit=6)
            if not value.isError():
                values.extend(value.bits)
            if len(values):
                query = """
                    INSERT INTO airtable(device_id,infanstatus01,infanstatus02,exfanstatus01,exfanstatus02,compstatus,heaterstatus,infanspeed01,infanspeed02,extfanspeed01,extfanspeed02,returntemp,retunhumi,ambienttemp,voldc,volac,compressorcurrent,heatercurrent,compressorspeed,compressorfre,dcpowercurrent,e01,e02,e03,e04,e05,e06,e07,e08,e09,e10,e11,e12,e13,e14,e15,e16,e17,e18,e19,e20,e21,e22,e23,e24,e26,e27,e28,e31,e32,e33,e34,timestamp)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
                params = ('air', values[0], values[1], values[2], values[3], values[4], values[5], values[32], values[33], values[34], values[35], values[36], values[37], values[38], values[46], values[47], values[48], values[49], values[50], values[53], values[55], values[56], values[57], values[58], values[59], values[60], values[61], values[62],
                          values[63], values[64], values[65], values[66], values[67], values[68], values[69], values[70], values[71], values[72], values[73], values[74], values[75], values[76], values[77], values[78], values[79], values[81], values[82], values[83], values[86], values[87], values[88], values[89], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                run(query, params)
        return {"air":[
            {"status":True}
        ]}

    except:
        print("connect  timeout ...!")


def snmp_pdu():
    try:
        listParamsPdu = ["AlarmCount", "WarnCount", "Manufacturer", "MainSerial", "MainName", "MainLabel", "MainAvail", "MeterType", "TotalName", "TotalLabel", "TotalRealPower", "TotalApparentPower", "TotalPowerFactor", "TotalEnergy", "PhaseName", "PhaseLabel",
                         "PhaseVoltage", "PhaseCurrent", "PhaseRealPower", "PhaseApparentPower", "PhasePowerFactor", "PhaseEnergy", "PhaseBalance", "PhaseCurrentCrestFactor", "BreakerName", "BreakerName", "BreakerLabel", "BreakerLabel", "BreakerCurrent", "BreakerCurrent"]
        listParamsPduvaluesbase = ['alarmcount', 'warncount', 'manufacturer', 'mainserial', 'mainname', 'mainlabel', 'mainavail', 'metertype', 'totalname', 'totallabel', 'totalrealpower', 'totalapparentpower', 'totalpowerfactor', 'totalenergy', 'phasename', 'phaselabel',
                                   'phasevoltage', 'phasecurrent', 'phaserealpower', 'phaseapparentpower', 'phasepowerfactor', 'phaseenergy', 'phasebalance', 'phasecurrentcrestfactor', 'breakername01', 'breakername02', 'breakerlabel01', 'breakerlabel02', 'breakercurrent01', 'breakercurrent02']
        listOdiPdu = [".1.3.6.1.4.1.21239.5.2.1.12.0", ".1.3.6.1.4.1.21239.5.2.1.13.0", ".1.3.6.1.4.1.21239.5.2.1.14.0", ".1.3.6.1.4.1.21239.5.2.1.15.0", ".1.3.6.1.4.1.21239.5.2.3.1.1.2.1", ".1.3.6.1.4.1.21239.5.2.3.1.1.3.1", ".1.3.6.1.4.1.21239.5.2.3.1.1.4.1", ".1.3.6.1.4.1.21239.5.2.3.1.1.5.1", ".1.3.6.1.4.1.21239.5.2.3.1.1.6.1", ".1.3.6.1.4.1.21239.5.2.3.1.1.7.1", ".1.3.6.1.4.1.21239.5.2.3.1.1.8.1", ".1.3.6.1.4.1.21239.5.2.3.1.1.9.1",
                      ".1.3.6.1.4.1.21239.5.2.3.1.1.10.1", ".1.3.6.1.4.1.21239.5.2.3.1.1.11.1", ".1.3.6.1.4.1.21239.5.2.3.1.1.12.1", ".1.3.6.1.4.1.21239.5.2.3.2.1.2.1", ".1.3.6.1.4.1.21239.5.2.3.2.1.3.1", ".1.3.6.1.4.1.21239.5.2.3.2.1.4.1", ".1.3.6.1.4.1.21239.5.2.3.2.1.8.1", ".1.3.6.1.4.1.21239.5.2.3.2.1.12.1", ".1.3.6.1.4.1.21239.5.2.3.2.1.13.1", ".1.3.6.1.4.1.21239.5.2.3.2.1.14.1", ".1.3.6.1.4.1.21239.5.2.3.2.1.15.1",
                      ".1.3.6.1.4.1.21239.5.2.3.2.1.17.1", ".1.3.6.1.4.1.21239.5.2.3.2.1.19.1", ".1.3.6.1.4.1.21239.5.2.3.3.1.2.1", ".1.3.6.1.4.1.21239.5.2.3.3.1.2.2", ".1.3.6.1.4.1.21239.5.2.3.3.1.3.1", ".1.3.6.1.4.1.21239.5.2.3.3.1.3.2", ".1.3.6.1.4.1.21239.5.2.3.3.1.4.1"]
        results = []
        for x in range(1, 3):
            data = []
            its = get_bulk('192.168.112.24'+str(x), listOdiPdu)
            for it in its:
                for k, v in it.items():
                    data.append(v)
            device_id = "pdu_0"+str(x)
            values = {}
            if len(data) > 0:
                query = """
                INSERT INTO pdutable(status,device_id,alarmcount,warncount,manufacture,mainserial,mainname,mainlabel,mainavail,metertype,totalname,totallabel,totalrealpower,totalapparentpower,totalpowerfactor,totalenergy,phasename,phaselabel,
                                phasevoltage,phasecurrent,phaserealpower,phaseapparentpower,phasepowerfactor,phaseenergy,phasebalance,phasecurrentcrestfactor,breakername01,breakername02,breakerlabel01,breakerlabel02,breakercurrent01,breakercurrent02,timestamp)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
                params = (bool(1), device_id, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15],
                          data[16], data[17], data[18], data[19], data[20], data[21], data[22], data[23], data[24], data[25], data[26], data[27], data[28], data[29], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                run(query, params)
            for i in range(0, len(data)):
                values[listParamsPdu[i]] = data[i]
            results.append(values)
        return {
            "pdu": [
                {
                    "pdu_01": results[0]
                },
                {
                    "pdu_02": results[1]
                }
            ]
        }
    except:
        print("check error ..!")


def snmp_ups():
    try:
        listParamsUps = ["IdentManufacturer", "IdentModel", "SoftwareVersion", "IdentAgentSoftwareVersion", "IdentName", "IdentAttachedDevices", "BatteryStatus", "SecondsOnBattery", "EstimatedMinutesRemaining", "EstimatedChargeRemaining", "BatteryVoltage", "BatteryTemperature", "InputLineBads", "InputNumLines", "InputLineIndex", "InputFrequency", "InputVoltage",
                         "OutputSource", "OutputFrequency", "OutputNumLines", "OutputLineIndex", "OutputVoltage", "OutputPower", "OutputPercentLoad", "BypassFrequency", "BypassNumLines", "BypassVoltage", "AlarmsPresent", "TestId", "TestSpinLock", "TestResultsSummary", "TestResultsDetail", "TestStartTime", "TestElapsedTime", "ShutdownAfterDelay", "StartupAfterDelay", "RebootWithDuration"]
        listParmasUpsDatabase = ['manufacturer', 'identmodel', 'softversion', 'agentsoftversion', 'identname', 'attacheddevices', 'batstatus', 'secondsonbat', 'estiminutesremain', 'estichargeremain', 'batvoltage', 'battemp', 'inputlinebads', 'inputnumlines', 'inputlineindex', 'inputfreq', 'inputvoltage',
                                 'outputsource', 'outfreq', 'outnumlines', 'outlineindex', 'outvoltage', 'outpower', 'outpercentload', 'bypassfreq', 'bypassnumlines', 'bypassvoltage', 'alarmspresent', 'testid', 'testspinlock', 'testresultssummary', 'testresultsdetail', 'teststarttime', 'testelapsedtime', 'shutafterdelay', 'startafterdelay', 'rebootwithduration']
        listOidUps = [".1.3.6.1.2.1.33.1.1.0.0", ".1.3.6.1.2.1.33.1.1.1.0", ".1.3.6.1.2.1.33.1.1.2.0", ".1.3.6.1.2.1.33.1.1.3.0", ".1.3.6.1.2.1.33.1.1.4.0", ".1.3.6.1.2.1.33.1.1.5.0", ".1.3.6.1.2.1.33.1.1.6.0", ".1.3.6.1.2.1.33.1.2.1.0", ".1.3.6.1.2.1.33.1.2.2.0", ".1.3.6.1.2.1.33.1.2.3.0", ".1.3.6.1.2.1.33.1.2.4.0", ".1.3.6.1.2.1.33.1.2.5.0", ".1.3.6.1.2.1.33.1.2.7.0", ".1.3.6.1.2.1.33.1.3.1.0", ".1.3.6.1.2.1.33.1.3.2.0", ".1.3.6.1.2.1.33.1.3.3.1.1.1", ".1.3.6.1.2.1.33.1.3.3.1.2.1", ".1.3.6.1.2.1.33.1.3.3.1.3.1", ".1.3.6.1.2.1.33.1.4.1.0",
                      ".1.3.6.1.2.1.33.1.4.2.0", ".1.3.6.1.2.1.33.1.4.3.0", ".1.3.6.1.2.1.33.1.4.4.1.1.1", ".1.3.6.1.2.1.33.1.4.4.1.2.1", ".1.3.6.1.2.1.33.1.4.4.1.4.1", ".1.3.6.1.2.1.33.1.4.4.1.5.1", ".1.3.6.1.2.1.33.1.5.1.0", ".1.3.6.1.2.1.33.1.5.2.0", ".1.3.6.1.2.1.33.1.5.3.1.2.1", ".1.3.6.1.2.1.33.1.6.1.0", ".1.3.6.1.2.1.33.1.7.1.0", ".1.3.6.1.2.1.33.1.7.2.0", ".1.3.6.1.2.1.33.1.7.3.0", ".1.3.6.1.2.1.33.1.7.4.0", ".1.3.6.1.2.1.33.1.7.5.0", ".1.3.6.1.2.1.33.1.7.6.0", ".1.3.6.1.2.1.33.1.8.2.0", ".1.3.6.1.2.1.33.1.8.3.0"]
        data = []
        its = get_bulk('192.168.112.172', listOidUps)
        for it in its:
            for k, v in it.items():
                data.append(v)
        values = {"device": "ups"}
        if len(data) > 0:
            query = """
            INSERT INTO upstable(device_id, manufacturer, identmodel, softversion, agentsoftversion, identname, attacheddevices, batstatus, secondsonbat, estiminutesremain, estichargeremain, batvoltage, battemp, inputlinebads, inputnumlines, inputlineindex, inputfreq, inputvoltage,
                                 outputsource, outfreq, outnumlines, outlineindex, outvoltage, outpower, outpercentload, bypassfreq, bypassnumlines, bypassvoltage, alarmspresent, testid, testspinlock, testresultssummary, testresultsdetail, teststarttime, testelapsedtime, shutafterdelay, startafterdelay, rebootwithduration,timestamp)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            params = ('ups', data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19], data[20],
                      data[21], data[22], data[23], data[24], data[25], data[26], data[27], data[28], data[29], data[30], data[31], data[32], data[33], data[34], data[35], data[36], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            run(query, params)
        for i in range(0, len(data)):
            values[listParamsUps[i]] = data[i]
        return values
    except:
        print("check error ..!")

def modbus():
    data = {
        "smartcabinet": [
            # read_temp(),
            # readStatusFan(),
            # readSmoke(),
            # readDoor(),
            # readLeak(),
            #snmp_pdu(),
            snmp_ups(),
            # readAir(),
            # readPmu(),
            {'test':"like"}
        ],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    print(data)
    # infor = infor_mqtt()
    # if infor[0]['status']=='on':
    #     connect_mqtt(infor[0]['topic'],json.dumps(data))


# function  alarm
def alarm():
    while True:
        time.sleep(1)
        i = random.randint(2, 9)
        if i > 5:
            query = """
            INSERT INTO alarmtable(device,type,discription,timestamp)
            VALUES(%s,%s,%s,%s)
            """
            params = ('pdu', 'error', 'disconnect power',
                      datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            run(query, params)

if __name__ == "__main__":
    while True:
        modbus()
