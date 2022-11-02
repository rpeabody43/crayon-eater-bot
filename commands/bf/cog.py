import discord
from discord import app_commands
from discord.ext import commands
from . import brainf

class BrainFCog (commands.Cog):
    """
    A Discord bot cog to add a BrainF&#@ interpreter

    Commands
    --------
    bf:
        takes in bf string, returns ASCII
    """
    
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name='bf',
        description='Interpret some bf code, returns and ASCII string'
    )
    async def bf(self, interaction: discord.Interaction, code: str):
        response = ''
        try:
            response = f'```fix\n{brainf.interpret(code)}```'
        except MemoryError:
            response = '*`Failed to compile: Memory Error`*'
        except ValueError:
            response = '*`Failed to compile: Value Error`*'
        except:
            response = '*`Failed to compile`*'
        await interaction.response.send_message(response)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BrainFCog(bot))