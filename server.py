#!/usr/bin/env python

import os

import paho.mqtt.client as mqtt
from blinkstick import blinkstick

stick = blinkstick.find_first()


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
    assert len(slugs) > 2, "too few elements : %s" % slugs
    if len(slugs) == 3:
        index = int(slugs[2])
        if body.startswith(b"#"):
            hex = body.decode()
            print(index, hex)
            stick.set_color(index=index, hex=hex)
        else:
            print(index, body)
            stick.set_color(index=index, name=body.decode())


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
