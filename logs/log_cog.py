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
            await interaction.response.send_message("`logfile not found`")
            return
        rgx = '\[202[0-9]-[0-1][0-9]-[0-3][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]\]'
        matches = list(re.finditer(rgx, logs))
        first_log = len(matches)-x
        ret = logs[matches[first_log].start():] if first_log >= 0 else logs
        await interaction.user.send(f'```ini\n{ret}```')
        await interaction.response.send_message('`logs sent`')



async def setup (bot: commands.Bot) -> None:
    await bot.add_cog(LogCog(bot))
