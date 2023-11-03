"""Simulates running pmc_thermos_m7_rc"""

import random
import paho.mqtt.client as mqtt
from time import sleep

def on_connect(client, obj, flags, rc):
    print("Connected...")

def on_subscribe(client, obj, mid, qos):
    print("Subscribed...")

def on_message(client, obj, msg):
    print(msg.topic + " " + msg.payload.decode('utf-8'))


client = mqtt.Client("pmcClient0")
client.on_message = on_message
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.connect("192.168.1.60", 1883, 60)
client.subscribe("test/activate", 0)

client.loop_start()

sleep(10)

while True:
    sleep(1)
    t1 = t2 = t3 = random.uniform(20,30)    
    simulated_message = f"PMC0, {t1:.2f}, {t2:.2f}, {t3:.2f}"
    print(simulated_message)
    client.publish("test/thermos", simulated_message, qos=0)

