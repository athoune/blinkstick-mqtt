#!/usr/bin/env python

import re

import paho.mqtt.client as mqtt
from blinkstick import blinkstick

stick = blinkstick.find_first()
SPACES = re.compile(r"\s+")


# The callback for when the client receives a CONNACK response from the server.
def listen(name=""):
    print(f"Listening {name}")
    name = f"/{name}/#"

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # client.subscribe("$SYS/#")
        client.subscribe(f"blinkstick{name}")

    return on_connect


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    slugs = msg.topic.split("/", 128)
    if slugs[0] == "blinkstick":
        on_blinkstick(slugs, msg.payload)
    print(msg.topic + " " + str(msg.payload))


def on_blinkstick(slugs, body):
    "blinkstick handler"
    print("slugs", slugs, body)
    assert len(slugs) >= 3, f"too few elements : {slugs}"
    if slugs[2] == "off":
        for i in range(8):
            stick.set_color(index=i + 1, name="black")
        return
    if slugs[2] == "-":
        index = range(1, 9)
    else:
        index = [int(i) for i in slugs[2].split(",")]
    colors = SPACES.split(body.decode()) * 8
    if slugs[3] in ("color", "morph"):
        if slugs[3] == "color":
            action = stick.set_color
        elif slugs[3] == "morph":
            action = stick.morph
        print("colors", colors)
        for i, idx in enumerate(index):
            color = colors[i]
            if color.startswith("#"):
                action(index=idx, hex=color)
            else:
                action(index=idx, name=color)


client = mqtt.Client()
client.on_message = on_message

if __name__ == "__main__":
    import os

    client.on_connect = listen(os.getenv("NAME") or "")
    client.connect(os.getenv("LISTEN") or "localhost", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()
