from discord.ext import commands

# todo:Themi Make this part of a bigger "Core" class with other "core" commands

class Ping:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Pong!"""
        await ctx.send("Pong!")


def setup(bot):
    bot.add_cog(Ping(bot))
