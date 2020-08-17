import discord
import requests
import json
from discord.ext import commands
import requests

class steam(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def playercount(self, ctx, args):
        
        player_count_url = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={args}")
        data_json = player_count_url.json()

        player_count = data_json['response']['player_count']
        
        await ctx.send("There are {0} concurrent players".format(player_count))
        

def setup(client):
    client.add_cog(steam(client))
    print("Steam.py loaded")