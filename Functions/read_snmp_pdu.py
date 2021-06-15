import os
import time
from datetime import datetime
from Configs.db import run, connection
from Configs.snmp import get, get_bulk, get_bulk_auto


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
        print("connect succcessfully !")
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
        print("connect failed!")


if __name__ == "__main__":
    for i in range(1, 3):
        hostname = "192.168.112.24"+str(i)
        response = os.system("ping " + hostname)
    while response == 0:
        snmp_pdu()
        time.sleep(1)
