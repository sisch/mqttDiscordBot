import asyncio
import datetime

import paho.mqtt.client as mqtt

import config


class MQTTConnection:
    def __init__(self, debug=False):
        from config import MQTT_USER, MQTT_PASSWORD, MQTT_HOST, MQTT_PORT

        self.on_message_callbacks = [self.log_message]
        self.client = mqtt.Client("Discord Bot")
        if MQTT_USER != "":
            self.client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        self.client.connect(MQTT_HOST, MQTT_PORT)
        self.DEBUG = debug
        self.client.on_message = self.on_message

    def log_message(self, message):
        self.debug_log(
            f"[{datetime.datetime.now()}] {message}"
        )

    def debug_log(self, message):
        if self.DEBUG:
            print(message)

    def add_listener(self, func):
        if not func in self.on_message_callbacks:
            self.on_message_callbacks.append(func)

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode("utf-8")
        if topic in config.MQTT_SUBSCRIBERS.keys():
            template, func = config.MQTT_SUBSCRIBERS[topic]
            payload = template.format(value=func(topic, payload))
        for callback in self.on_message_callbacks:
            callback(payload)

    def send_command(self, topic, payload, retain=False):
        self.client.publish(topic, payload, retain=retain)
