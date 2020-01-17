import discord
import random
from discord.ext import commands

client = commands.Bot(command_prefix = "h?")

@client.event
async def on_ready():
    print("I liek pie===")

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


client.run("NjY3MzgzNDI4NzY0Nzk0ODgx.XiB7lA.OODcVVaJ85TEpuN2BsKDfXci5L0")