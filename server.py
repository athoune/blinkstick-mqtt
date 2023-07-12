#!/usr/bin/env python

import re

import paho.mqtt.client as mqtt
from blinkstick import blinkstick

stick = blinkstick.find_first()
SPACES = re.compile(r"\s+")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    client.subscribe("blinkstick/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    slugs = msg.topic.split("/", 128)
    if slugs[0] == "blinkstick":
        on_blinkstick(slugs, msg.payload)
    print(msg.topic + " " + str(msg.payload))


def on_blinkstick(slugs, body):
    print("slugs", slugs, body)
    assert len(slugs) >= 3, "too few elements : %s" % slugs
    if slugs[2] == "off":
        for i in range(8):
            stick.set_color(index=i+1, name='black')
        return
    if slugs[2] == "-":
        index = range(1, 9)
    else:
        index = [int(i) for i in slugs[2].split(",")]
    if slugs[3] == "color":
        colors = SPACES.split(body.decode()) * 8
        print("colors", colors)
        for i, idx in enumerate(index):
            color = colors[i]
            if color.startswith("#"):
                stick.set_color(index=idx, hex=color)
            else:
                stick.set_color(index=idx, name=color)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
