import discord
import random
import datetime
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = "h?")
status = cycle(["Hello World", "Are these the internets?", "Ask me anything!", "3.521% sugar", "From the streets of Lubina!", "80% bug free!"])

now = datetime.datetime.now()
text1 = now.strftime("%D, %H:%M:%S")


@client.event
async def on_ready():
    print("I liek pie===")
    change_status.start()
    print(text1)

@tasks.loop(seconds=30)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_member_join(member):
    print(f"{member} has joined the server.")
    await client.send(f"{member} has joined the server :PogU:")

@client.event
async def on_member_remove(member):
    print(f"{member} has left the server.")
    await client.send(f"{member} has left the server :WeirdChamp:")

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
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention} for {reason}")

@client.command()
async def unban(ctx, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            return

client.run("NjY3MzgzNDI4NzY0Nzk0ODgx.XiHZOQ.as66DriXzoSArSprykiKhI65bBA")