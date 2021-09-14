
import discord                      #boy I wonder what this is
from discord.ext import commands    #commands module of the discord api
import os                           #open .env files
from dotenv import load_dotenv

bot = commands.Bot(command_prefix="$") #creating a bot instance, the connection to discord
bot.load_extension('Commands.TwitchIntegration')
        
load_dotenv()

#@bot.event is used to register an event
@bot.event
#on_ready is called when the bot is ready to be used (good for initialization)
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

bot.run(os.getenv('DiscordToken')) #test comment funny haha