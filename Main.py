
import discord  # boy I wonder what this is
from discord.ext import commands  # commands module of the discord api
import os  # open .env files
from dotenv import load_dotenv

# creating a bot instance, the connection to discord
bot = commands.Bot(command_prefix='$')
bot.load_extension('Commands.stream.TwitchCog')
bot.load_extension('Commands.bf.BrainFCog')

load_dotenv()

# @bot.event is used to register an event
# on_ready is called when the bot is ready to be used (good for initialization)
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


def main():
    bot.run(os.getenv('DiscordToken'))


if __name__ == '__main__':
    main()
