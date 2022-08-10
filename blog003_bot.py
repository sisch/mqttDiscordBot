import asyncio as asyncio
from threading import Thread

from blog003_mqtt_connection import MQTTConnection
import discord
import blog003_config

client = discord.Client()
mqtt_connection = MQTTConnection()


@client.event
async def on_ready():
    print(f"{client.user} has connected to {client.guilds[0].name}")
    mqtt_connection.client.publish(blog003_config.DISCORD_BOT_TOPIC, "online")


@client.event
async def on_message(message):
    if not message.content.startswith("!"):
        return
    await run_command(message)


async def send_message(message_string, channel=None):
    if channel is None:
        channel = await client.fetch_channel(blog003_config.DISCORD_BOT_CHANNEL_ID)
    await channel.send(message_string)


async def run_command(message):
    for command, mqtt_commands in blog003_config.COMMANDS.items():
        if command in message.content:
            for (topic, payload, feedback) in mqtt_commands:
                if topic:
                    mqtt_connection.client.publish(topic, payload)
                if feedback:
                    await send_message(feedback)
            return


def send_mqtt_to_discord(message_string, channel=None):
    asyncio.run_coroutine_threadsafe(send_message(message_string, channel), client.loop)


def setup_subscribers_and_callback():
    for topic in blog003_config.MQTT_SUBSCRIBERS.keys():
        mqtt_connection.add_subscriber(topic)
    mqtt_connection.set_discord_callback(send_mqtt_to_discord)


def start_both_async():
    mqtt_thread = Thread(mqtt_connection.client.loop_start())
    mqtt_thread.start()
    discord_thread = Thread(client.run(blog003_config.DISCORD_TOKEN))
    discord_thread.start()


if __name__ == "__main__":
    setup_subscribers_and_callback()
    start_both_async()
