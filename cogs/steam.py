import discord
import re
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import datetime

class steam(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def steam(self, ctx, args):
        URL = f"https://steamcommunity.com/id/{args}"
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        steam_name = soup.find('span', {'class': 'actual_persona_name'}).get_text()
        steam_picture = soup.find('img', {'src': re.compile('.jpg')})
        steam_level = soup.find('span', {'class': 'friendPlayerLevelNum'}).get_text()
        steam_activity = soup.find('div', {'class': 'recentgame_quicklinks recentgame_recentplaytime'}).get_text()


        embed = discord.Embed(colour=ctx.author.colour, timestamp=datetime.datetime.utcnow())

        embed.set_image(url=steam_picture['src'])

        embed.add_field(name="Steam name:", value=steam_name.strip(), inline=False)
        embed.add_field(name="Steam level:", value=steam_level.strip(), inline=False)
        embed.add_field(name="Recent activity:", value=steam_activity.strip(), inline=False)
        embed.set_footer(text=f"Requested By: {ctx.author.name}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(steam(client))
    print("Steam.py loaded")