import paho.mqtt.client as mqtt
from .db import run, connection
import pandas as pd
import time

def infor_mqtt():
    df_new = pd.DataFrame([])
    query = """
        SELECT *
        FROM mqtttable
        ORDER BY id DESC LIMIT 1
        """
    df = pd.read_sql(query, con=connection)
    if len(df) > 0:
        df_new = pd.concat([df_new, df])
        df_new = df_new.to_dict(orient='records')
    return df_new

data = infor_mqtt()
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection to Broker {}:{} Successfully!".format(data[0]["host"],int(data[0]['port'])))
    client.subscribe("/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# connect to broker
client = mqtt.Client()
client.connect(data[0]["host"],int(data[0]['port']), 60)
client.username_pw_set(data[0]['username'],data[0]['password'])

def connect_mqtt(topic,payload):
    client.on_connect = on_connect
    client.on_message = on_message
    client.publish(topic=topic,payload=payload)    #publish payload
    client.loop_start()