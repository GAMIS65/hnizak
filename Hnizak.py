import discord
import youtube_dl
import random
import datetime
from discord.utils import get
from discord.ext import commands

client = commands.Bot(command_prefix = "h?")

now = datetime.datetime.now()
text1 = now.strftime("%D, %H:%M:%S")

@client.event
async def on_ready():
    print("I liek pie===")
    await client.change_presence(activity=discord.Game("Python"), status=discord.Status.online)
    print(text1)

@client.event
async def on_member_join(member):
    print(f"{member} has joined the server.")

@client.event
async def on_member_remove(member):
    print(f"{member} has left the server.")

@client.command(brief='Latency of the bot', description='Latency of the bot')
async def latency(ctx):
    await ctx.send(f"{round(client.latency * 1000)}ms")

@client.command()
async def ask(ctx):
    responses = ["Yes",
                 "No",]
    await ctx.send(f"{random.choice(responses)}")

@client.command(brief='Delete messages', description='Delete messages')
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit=amount)

@client.command()
async def uptime(ctx):
    await ctx.send(f"The bot is UP since {text1}")

@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"Joined {channel}")

@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")

client.run("NjY3MzgzNDI4NzY0Nzk0ODgx.XiB7lA.OODcVVaJ85TEpuN2BsKDfXci5L0")