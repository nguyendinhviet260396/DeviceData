import os
import time
from datetime import datetime
from Configs.db import run, connection
from Configs.snmp import get, get_bulk, get_bulk_auto


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
        print(values)
        return values
    except:
        print("check error ..!")

# if __name__ == "__main__":
#     while True:
#         hostname = "192.168.112.172"
#         response = os.system("ping " + hostname)
#         # and then check the response...
#         if response == 0:
#             print(hostname, 'is up!')
#             snmp_ups()
#         else:
#             print(hostname, 'is down!')
#         time.sleep(1)

if __name__ == "__main__":
    hostname = "192.168.112.172"
    response = os.system("ping " + hostname)
    while response == 0:
        snmp_ups()
        time.sleep(1)
