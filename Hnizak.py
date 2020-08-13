# imports
import discord
import datetime
import os
import dotenv
from discord.ext import commands, tasks
from itertools import cycle
from dotenv import load_dotenv


# Token
load_dotenv()
TOKEN = "NjY3MzgzNDI4NzY0Nzk0ODgx.XiB7QA.Z5ygNpIr0omvCp_FpD86Dy7gLGE"

# Command prefix
client = commands.Bot(command_prefix="h?")


# Status splash text
status = cycle([line.rstrip('\n') for line in open("splash.txt")])


# Time
now = datetime.datetime.now()
text1 = now.strftime("%D, %H:%M:%S")


# Load cog
@client.command()
@commands.is_owner()
async def load(ctx, exetension):
    client.load_extension(f"cogs.{exetension}")


# Reload cog
@client.command()
@commands.is_owner()
async def reload(ctx, exetension):
    client.unload_extension(f"cogs.{exetension}")
    client.load_extension(f"cogs.{exetension}")


# Ready
@client.event
async def on_ready():
    print("I liek pie===")
    change_status.start()
    print(text1)


# Change status every 30 seconds
@tasks.loop(seconds=30)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))



for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)