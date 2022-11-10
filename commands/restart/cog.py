import discord
from discord import app_commands
from discord.ext import commands
import subprocess
import sys

class RestartCog (commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name='restart',
        description='restarts the bot; only available to select admins'
    )
    # replace arg: int with the appropriate parameter and type for your command
    async def restart(self, interaction: discord.Interaction):
        cmd = '/home/ryan/crayon-eater-bot/run.sh'
        await interaction.response.send_message('`restarting...`')
        subprocess.Popen(cmd, shell=True, executable='/bin/bash')
        sys.exit()

async def setup (bot: commands.Bot) -> None:
    await bot.add_cog(RestartCog(bot))