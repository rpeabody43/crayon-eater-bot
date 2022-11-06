import discord
from discord import app_commands
from discord.ext import commands
import Paginator
from datetime import datetime

from .leaderboard import update, fmt

class OldHallCog (commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name='most-oldhall',
        description='Get the leaderboard for the teachers that have been out the most'
    )
    async def most_old_hall(self, interaction: discord.Interaction):
        update()
        leaderboard = fmt()
        pages = []

        for i in range((len(leaderboard) // 5) + 1):
            start = i*5
            limit = len(leaderboard) - start
            if limit > 5: limit = 5

            embed=discord.Embed(
                title='**AHS Old Hall Leaderboard**',
                color=0x7c0c10
                )
            for j in range(limit):
                k = list(leaderboard.keys())[start+j]
                v = leaderboard[k]
                embed.add_field(name=k, value=str(v), inline=False)
            # the logo hosted on discord because it's easy
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/824741381578162201/1038939780110626937/logo.png')
            embed.set_footer(text=f"Last updated {datetime.now().strftime('%m/%d/%Y at %H:%M')}")
            pages.append(embed)

        await Paginator.Simple().start(interaction, pages=pages)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OldHallCog(bot))
