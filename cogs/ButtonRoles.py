from discord.ext import commands


class ButtonRoles:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role("Mod")
    async def buttonroles(self, cxt, text: str):
        """Pong!"""
        await self.bot.say("Pong! " + text)


def setup(bot):
    bot.add_cog(ButtonRoles(bot))
