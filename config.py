MQTT_HOST: str = "127.0.0.1"
MQTT_PORT: int = 1883
MQTT_USER: str = ""
MQTT_PASSWORD: str = ""

DISCORD_BOT_TOPIC = "bot/discord/state"
DISCORD_TOKEN = "define in secrets.py"
DISCORD_LINK = "define in secrets.py"



COMMANDS = {
    'toggle_power_socket_leds_couch': ("cmnd/office/socket1/POWER", "TOGGLE"),
    'toggle_wind': ("cmnd/office/fansocket/POWER", "TOGGLE"),
}


try:
    from . import secrets
except ImportError as e:
    print(e.msg)
