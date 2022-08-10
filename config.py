import os
from dotenv import load_dotenv
import mqtt_subscribers as subs

load_dotenv()

MQTT_HOST: str = os.getenv("MQTT_HOST")
MQTT_PORT: int = int(os.getenv("MQTT_PORT"))
MQTT_USER: str = os.getenv("MQTT_USER")
MQTT_PASSWORD: str = os.getenv("MQTT_PASSWORD")
DISCORD_BOT_TOPIC: str = os.getenv("DISCORD_BOT_TOPIC", "bot/discord/state")
DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN")

DISCORD_BOT_CHANNEL_ID = 977968510091288667
DISCORD_BOT_REPLY_CHANNEL_ID = 977968510091288667

# Precedence:
# User required (any) > Roles required(all) > roles allowed (any)
# All of these lists take user/role IDs
DISCORD_USER_ID_REQUIRED = []
DISCORD_ROLES_REQUIRED = []
DISCORD_ROLE_REQUIRED = [977957959982256158]


COMMANDS = {
    "t_arbeitszimmer": [("cmnd/office/temperature1/status", "10", "")],
    "steckdose_ventilator_an": [("cmnd/office/fansocket/POWER", "on", "")],
    "steckdose_ventilator_aus": [("cmnd/office/fansocket/POWER", "off", "")],
    "steckdose_ventilator_schalten": [("cmnd/office/fansocket/POWER", "toggle", "")],
    "led_lagerfeuer": [("OneNightLamp/in", "?47", ""),       # geschwindigkeit
                       ("OneNightLamp/in", "%18", ""),       # helligkeit
                       ("OneNightLamp/in", "#00FF4400", ""), # primärfarbe
                       ("OneNightLamp/in", "/48", "")
                       ],      # animation Lagerfeuer
    "led_breath_red": [("OneNightLamp/in", "?92", ""),
                       ("OneNightLamp/in", "%25", ""),
                       ("OneNightLamp/in", "#00FF1000", ""),  # tiefes Rot
                       ("OneNightLamp/in", "##00000000", ""),  # schwarz
                       ("OneNightLamp/in", "/2", "")
                       ],
}

MQTT_SUBSCRIBERS = {
    "stat/office/temperature1/STATUS10": ("Es ist {value}°C", subs.bmp180_temperature),
    "stat/office/fansocket/POWER": ("Die Ventilator Steckdose ist {value}", subs.direct),
}


def bmp180_temperature(topic, payload):
    import json
    json_tree = json.loads(payload)
    temperature = json_tree["StatusSNS"]["BMP180"]["Temperature"]
    return temperature


def direct(topic, payload):
    return payload
