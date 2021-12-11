import discord
from discord.ext import commands

# arg must be a string


def brainf_string(arg):
    turing_machine = [0] * 100
    pointer = 0
    chars = []
    i = 0

    while i < len(arg):
        if turing_machine[pointer] > 255 or turing_machine[pointer] < 0:
            raise ValueError("Only int values between 0 and 255")

        elif arg[i] == '<':
            if pointer <= 0:
                raise MemoryError
            pointer -= 1

        elif arg[i] == '>':
            pointer += 1

        elif arg[i] == '+':
            turing_machine[pointer] += 1

        elif arg[i] == '-':
            if turing_machine[pointer] > 0:
                turing_machine[pointer] -= 1

        elif arg[i] == '.':
            chars.append(turing_machine[pointer])

        elif arg[i] == '[':
            if turing_machine[pointer] == 0:
                loop = 1
                while loop > 0:
                    i += 1
                    if arg[i] == '[':
                        loop += 1
                    elif arg[i] == ']':
                        loop -= 1

        elif arg[i] == ']':
            loop = 1
            while loop > 0:
                i -= 1
                if arg[i] == '[':
                    loop -= 1
                elif arg[i] == ']':
                    loop += 1
            i -= 1

        i += 1

    return_str = ""
    for i in chars:
        return_str += chr(i)
    # return_str = chars
    return return_str


class BrainFCog (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bf(self, ctx, *, arg):
        await ctx.reply('```fix\n' + brainf_string(arg) + '```')

    @bf.error
    async def bf_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('$bf (brainf code)')

        if isinstance(error, MemoryError):
            await ctx.reply('*`Failed to compile: Memory Error`*')
        if isinstance(error, ValueError):
            await ctx.reply('*`Failed to compile: Value Error`*')

        else:
            await ctx.send('*`Failed to compile`*')
        print("", str(ctx.message.jump_url), str(error), sep='\n')


def setup(bot):
    bot.add_cog(BrainFCog(bot))
