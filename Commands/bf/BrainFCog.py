from discord.ext import commands
import Commands.bf.BrainF as BrainF

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

    @commands.command()
    async def bf(self, ctx, *, arg):
        await ctx.reply('```fix\n' + BrainF.interpret(arg) + '```')

    @bf.error
    async def bf_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('$bf (brainf code)')

        elif isinstance(error, MemoryError):
            await ctx.reply('*`Failed to compile: Memory Error`*')
        elif isinstance(error, ValueError):
            await ctx.reply('*`Failed to compile: Value Error`*')

        else:
            await ctx.send('*`Failed to compile`*')
        print("", str(ctx.message.jump_url), str(error), sep='\n')


def setup(bot):
    bot.add_cog(BrainFCog(bot))