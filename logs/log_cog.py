import discord
from discord import app_commands
from discord.ext import commands
import re

class LogCog (commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name='logs',
        description='dms you the last x logs'
    )
    async def logs(self, interaction: discord.Interaction, x: int):
        logs: str
        try:
            with open ('logs/discord.log', 'r') as f:
                logs = f.read()
        except FileNotFoundError:
            interaction.response.send_message("`logfile not found`")
            return
        



async def setup (bot: commands.Bot) -> None:
    await bot.add_cog(LogCog(bot))
