import discord
from discord.ext import commands
import aiohttp

import os
from dotenv import load_dotenv

load_dotenv()

class CrayonBot (commands.Bot):
    
    def __init__(self):
        super().__init__(
            command_prefix='$',
            intents = discord.Intents.all(),
            application_id = 839290702331641907
        )

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        
        # loading commands
        everything = os.listdir('commands')
        to_load = [f'commands.{x}.cog' for x in everything if x != '__pycache__']
        for command in to_load:
            await self.load_extension(command)
            print (f'{command} loaded')

        await self.tree.sync()

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        await self.change_presence(activity=discord.Game(name="Balls 3D"))

def main():
    bot = CrayonBot()
    bot.run(token=os.getenv('DiscordToken'))

if __name__  == '__main__':
    main()