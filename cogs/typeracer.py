import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import datetime

class typeracer(commands.Cog):
    def __init__(self, client):
        self.client = client

        @commands.command()
        async def typeracer(self, ctx, args):
            URL = f"https://data.typeracer.com/pit/profile?user={args}"
            headers = {
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
            page = requests.get(URL, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')

            # get all the data
            typeracer_log_in_name = soup.find("span", id="profileUsername").get_text()  # get log in name
            typeracer_nickname = soup.find("td", text="Name").find_next_sibling("td").text  # get nickname / real name
            typeracer_WPM_rounded = soup.find("span", id="profileWpmRounded").get_text()    # get average rounded WPM
            typeracer_races_completed = soup.find("td", text="Races Completed").find_next_sibling("td").text    # get races completed
            typeracer_skill_level = soup.find("td", text="Skill Level").find_next_sibling("td").text    # get skill level
            typeracer_experience_level = soup.find("td", text="Experience Level").find_next_sibling("td").text  # get experience level
            typeracer_racing_since = soup.find("td", text="Racing Since").find_next_sibling("td").text  # get profile age

            embed = discord.Embed(colour=ctx.author.colour, timestamp=datetime.datetime.utcnow())   # embed colour and timestamp

            # embed
            embed.add_field(name="Name:", value=typeracer_log_in_name, inline=False)
            embed.add_field(name="Nickname:", value=typeracer_nickname, inline=False)
            embed.add_field(name="Speed:", value=typeracer_WPM_rounded, inline=False)
            embed.add_field(name="Races completed:", value=typeracer_races_completed, inline=False)
            embed.add_field(name="Skill level:", value=typeracer_skill_level, inline=False)
            embed.add_field(name="Experience level:", value=typeracer_experience_level, inline=False)
            embed.add_field(name="Racing since:", value=typeracer_racing_since, inline=False)

            embed.set_footer(text=f"Requested By: {ctx.author.name}", icon_url=ctx.author.avatar_url)   # footer

            await ctx.send(embed=embed)

    def setup(client):
        client.add_cog(typeracer(client))
        print("typeracer.py loaded")