import os
from dotenv import load_dotenv
load_dotenv()

MQTT_HOST: str = os.getenv("MQTT_HOST")
MQTT_PORT: int = int(os.getenv("MQTT_PORT"))
MQTT_USER: str = os.getenv("MQTT_USER")
MQTT_PASSWORD: str = os.getenv("MQTT_PASSWORD")
DISCORD_BOT_TOPIC: str = os.getenv("DISCORD_BOT_TOPIC",  "bot/discord/state")
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
    'toggle_power_socket_leds_couch': ("cmnd/office/socket1/POWER", "TOGGLE", ""),
    'toggle_leds': ("guestbathroom/in", "toggle", ""),
    'toggle_wind': ("cmnd/office/fansocket/POWER", "TOGGLE", "Wind is changing!"),
    'set_leds': ("guestbathroom/in", "{value}", ""),
}

PERMANENT_SUBSCRIBES = {
    "stat/office/fansocket/POWER": "Der Wind ist jetzt {value}.",
    "test/topic": "Die Testnachricht lautet: {value}",
}
