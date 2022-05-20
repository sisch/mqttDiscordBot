import time
import paho.mqtt.client as mqtt
import config
from mqtt import MQTTConnection


def setup_subscribers(connection):
    pass


if __name__ == '__main__':
    mqtt_connection = MQTTConnection(True)
    setup_subscribers(mqtt_connection)
    mqtt_connection.send_command(config.DISCORD_BOT_TOPIC, "online")
    mqtt_connection.client.will_set(config.DISCORD_BOT_TOPIC, "offline")
