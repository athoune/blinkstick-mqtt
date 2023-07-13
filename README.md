# Blinkstick-mqtt

Expose a [blinkstick](https://www.blinkstick.com) throught [mqtt](https://en.wikipedia.org/wiki/MQTT).

## Try it

[mosquitto]( https://mosquitto.org/) is a cute mqtt broker and client, but you can use wathever works.

```bash
poetry install
poetry run LISTEN=127.0.0.1 NAME=bob server.py
mosquitto_pub -t blinkstick/bob/-/morph -m "blue"
```
