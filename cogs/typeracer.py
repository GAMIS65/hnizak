import discord
from discord.ext import commands
import requests
import datetime

class typeracer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def typeracer(self, ctx, args):
        typeracer = requests.get(f"https://data.typeracer.com/users?id=tr:{args}&universe=play")
        data_json = typeracer.json()
        
        average_speed = data_json['tstats']['recentAvgWpm']
        points = data_json['tstats']['points']
        total_average_speed = data_json['tstats']['wpm']
        best_race = data_json['tstats']['bestGameWpm']
        country = data_json.get('country')
        
        embed = discord.Embed(colour=ctx.author.colour,timestamp=datetime.datetime.utcnow())

        # embed
        embed.add_field(name="Name:", value=args, inline=False)
        embed.add_field(name="Nickname:", value=data_json.get('name'), inline=False)
        embed.add_field(name="Speed:", value=f"{round(average_speed)} WPM", inline=False)
        embed.add_field(name="Total average:", value=f"{round(total_average_speed)} WPM", inline=False)
        embed.add_field(name="Best race:", value=f"{round(best_race)} WPM", inline=False)
        embed.add_field(name="Games won:", value=data_json['tstats']['gamesWon'], inline=False)
        embed.add_field(name="Points:", value=round(points), inline=False)
        embed.add_field(name="Races completed:", value=data_json['tstats']['cg'], inline=False)
        embed.add_field(name="Country:", value=f':flag_' + country + ":", inline=False)
        embed.add_field(name="Experience level:", value="Typist " + str(data_json['tstats']['level'][1:]), inline=False)
        embed.set_footer(text=f"Requested By: {ctx.author.name}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(typeracer(client))
    print("typeracer.py loaded")