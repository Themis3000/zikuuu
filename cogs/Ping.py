from discord.ext import commands


class Ping:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ping(self):
        """Pong!"""
        await self.bot.say("Pong!")


def setup(bot):
    bot.add_cog(Ping(bot))
