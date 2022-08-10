MQTT_HOST = "10.0.0.123"
MQTT_PORT = 1883
MQTT_USER = "plant"
MQTT_PASSWORD = "programmer"
DISCORD_BOT_TOPIC = "bot/discord/state"
DISCORD_TOKEN = "..."

DISCORD_BOT_CHANNEL_ID = 977968510091288667
DISCORD_BOT_REPLY_CHANNEL_ID = 977968510091288667


def bmp180_temperature(topic, payload):
    import json
    json_tree = json.loads(payload)
    temperature = json_tree["StatusSNS"]["BMP180"]["Temperature"]
    return temperature


def direct(topic, payload):
    return payload


MQTT_SUBSCRIBERS = {
    "stat/office/temperature1/STATUS10": ("Es ist {value}°C", bmp180_temperature),
    "stat/office/fansocket/POWER": ("Die Ventilator Steckdose ist {value}", direct),
}


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
