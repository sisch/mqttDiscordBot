import paho.mqtt.client as mqtt
import blog003_config


class MQTTConnection:
    def __init__(self):
        self.client = mqtt.Client("Discord Bot")
        if blog003_config.MQTT_USER != "":
            self.client.username_pw_set(blog003_config.MQTT_USER, blog003_config.MQTT_PASSWORD)
        self.client.connect(blog003_config.MQTT_HOST, blog003_config.MQTT_PORT)

        self.client.on_message = self.on_message

    def on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8")
        topic = message.topic

        response, function = blog003_config.MQTT_SUBSCRIBERS.get(topic)
        processed_data = function(topic, payload)

        discord_message = response.format(value=processed_data)
        self.discord_callback(discord_message)

    def send_message(self, topic, payload):
        self.client.publish(topic, payload)

    def add_subscriber(self, topic):
        self.client.subscribe(topic)

    def set_discord_callback(self, function):
        self.discord_callback = function
