import json
import time

import paho.mqtt.client as mqtt

MQTT_HOST = "10.0.0.34"  # IP-Adresse oder Hostname des Brokers
MQTT_PORT = 1883
MQTT_USER = "plant"  # Wie in den Mosquitto Blogposts angelegt
MQTT_PASSWORD = "programmer"  # Wie in den Mosquitto Blogposts angelegt

BMP180_DATA_TOPIC = "stat/office/temperature1/STATUS10"
BMP180_POLL_TOPIC = "cmnd/office/temperature1/status"
BMP180_POLL_PAYLOAD = "10"


def create_configured_client():
    client = mqtt.Client("Mein Python MQTT Client")
    client.username_pw_set(username=MQTT_USER, password=MQTT_PASSWORD)
    client.connect(host=MQTT_HOST, port=MQTT_PORT)
    return client


def handle_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    if message.topic == BMP180_DATA_TOPIC:
        json_tree = json.loads(payload)
        temperature = json_tree["StatusSNS"]["BMP180"]["Temperature"]
        print(f"Es ist {temperature}°C")
    else:
        print("[UNHANDLED]", message.topic, payload)


def send_message(client, topic, payload):
    client.publish(topic, payload)


def setup_subscriptions(client, topic):
    client.on_message = handle_message
    client.subscribe(topic)


mqtt_client = create_configured_client()
setup_subscriptions(mqtt_client, BMP180_DATA_TOPIC)
send_message(mqtt_client, "test/topic", "Hallo Welt!")

while True:
    mqtt_client.loop()
    send_message(mqtt_client, BMP180_POLL_TOPIC, BMP180_POLL_PAYLOAD)
    time.sleep(1)
