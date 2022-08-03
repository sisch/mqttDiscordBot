import discord
import config
client = discord.Client()


@client.event
async def on_ready():
    print(f"{client.user} has connected to {client.guilds[0].name}")


@client.event
async def on_message(message):
    if not message.content.startswith("!"):
        return
    for command,reply in config.COMMANDS.items():
        if message.content.startswith(command):
            await message.channel.send(reply)
            return
    await message.channel.send(f"> {message.content}? \nDas habe ich nicht!")

client.run(config.DISCORD_TOKEN)
