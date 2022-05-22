import time

import asyncio as asyncio
from threading import Thread

import config
from mqtt import MQTTConnection
import discord

client = discord.Client()
mqtt_connection = MQTTConnection(True)

loop = asyncio.get_event_loop()


def send_mqtt_to_discord(topic: str, payload: bytes):
    payload = payload.decode("utf-8")
    asyncio.run_coroutine_threadsafe(_send_mqtt_to_discord(topic, payload), client.loop)


async def _send_mqtt_to_discord(topic: str, payload: str):
    print(f"message for {topic} with payload {payload}.")
    await send_message(config.PERMANENT_SUBSCRIBES[topic].format(value=payload))


def setup_subscribers(connection):
    topics = list()
    for topic in config.PERMANENT_SUBSCRIBES.keys():
        topics.append((topic, 1))
    mqtt_connection.client.subscribe(topics)
    print("subscribed to: " + ",".join([t[0] for t in topics]))
    mqtt_connection.add_listener(send_mqtt_to_discord)


@client.event
async def on_ready():
    print(f"{client.user} has connected to {client.guilds[0].name}")
    mqtt_connection.client.publish(config.DISCORD_BOT_TOPIC, "online")


@client.event
async def on_message(message):
    if message.content.startswith("!help"):
        await print_help(message.channel)
        return
    if message.content.startswith("!"):
        if check_user_or_role(message.author):
            await run_command(message)
        else:
            await send_message("Das ist nicht erlaubt!", channel=message.channel)


async def print_help(channel):
    response = "```\nAvailable Commands:\n" + "\n".join(f"!{c}" for c in config.COMMANDS.keys()) + "\n```"
    await send_message(response, reply=True)


def check_user_or_role(author):
    if len(config.DISCORD_USER_ID_REQUIRED) > 0:
        if author.id not in config.DISCORD_USER_ID_REQUIRED:
            return False

    elif len(config.DISCORD_ROLES_REQUIRED) > 0:
        author_role_ids = [role.id for role in author.roles]
        for req_role in config.DISCORD_ROLES_REQUIRED:
            if req_role not in author_role_ids:
                print("a role is not in the author roles" + ",".join([role.name for role in author.roles]))
                return False

    elif len(config.DISCORD_ROLE_REQUIRED) > 0:
        author_role_ids = [role.id for role in author.roles]
        if all(role_id not in config.DISCORD_ROLE_REQUIRED for role_id in author_role_ids):
            return False
    return True


async def run_command(message):
    for command, (topic, payload, feedback) in config.COMMANDS.items():
        if command in message.content:
            arguments = message.content.replace("!"+command, "").lstrip()
            mqtt_connection.client.publish(topic, payload.format(value=arguments))
            if feedback != "" and feedback is not None:
                await send_message(feedback, reply=True)
            return


async def send_message(message_string, reply=False, channel=None):
    if channel is not None:
        await channel.send(message_string)
        return
    if reply and config.DISCORD_BOT_REPLY_CHANNEL_ID != "":
        channel = await client.fetch_channel(config.DISCORD_BOT_REPLY_CHANNEL_ID)
    elif not reply and config.DISCORD_BOT_CHANNEL_ID != "":
        channel = await client.fetch_channel(config.DISCORD_BOT_CHANNEL_ID)
    else:
        return
    await channel.send(message_string)


def run_both_async():
    loop.create_task(client.run(config.DISCORD_TOKEN))
    loop.create_task(mqtt_connection.client.loop_forever())


def start_both_async():
    mqtt_thread = Thread(mqtt_connection.client.loop_start())
    mqtt_thread.start()
    discord_thread = Thread(client.run(config.DISCORD_TOKEN))
    discord_thread.run()


if __name__ == '__main__':
    setup_subscribers(mqtt_connection)
    start_both_async()
    while True:
        mqtt_connection.client.loop()
