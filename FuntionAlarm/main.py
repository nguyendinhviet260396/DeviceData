import time
import random
from datetime import datetime
from config.db import run,connection
import pandas as pd

def function_alarm_ups():
    try:
        query = """
        SELECT *
        FROM upstable
        ORDER BY id DESC LIMIT 1
        """
        df_ups = pd.read_sql(query, con=connection)
        if len(df_ups)> 0 :
            df_ups = df_ups.to_dict(orient='records')
            query = """
            SELECT *
            FROM setupstable
            ORDER BY id DESC LIMIT 1
            """
            df_set_ups = pd.read_sql(query, con=connection)
            df_set_ups = df_set_ups.to_dict(orient='records')
            if len(df_set_ups) > 0 :
                i = random.randint(2, 9)
                if i > 5:
                    query = """
                    INSERT INTO alarmtable(device,type,discription,timestamp)
                    VALUES(%s,%s,%s,%s)
                    """
                    params = ('pdu', 'error', 'disconnect power',
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    run(query, params)
    except Exception as e:
        print(e)
    



# function  alarm
def run_alarm():
    start = time.time()
    function_alarm_ups()
    stop = time.time()
    print(stop-start)

    # i = random.randint(2, 9)
    # if i > 5:
    #     query = """
    #     INSERT INTO alarmtable(device,type,discription,timestamp)
    #     VALUES(%s,%s,%s,%s)
    #     """
    #     params = ('pdu', 'error', 'disconnect power',
    #                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #     run(query, params)

if __name__ == '__main__':
    # while True:
    time.sleep(1)
    run_alarm()
