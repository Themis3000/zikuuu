from discord.ext import commands

# todo:Themi Make this actually function using a non json database with its own server.
# todo:Themi Make add/remove selection commands

class ButtonRoles:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role("Mod")
    async def buttonroles(self, cxt, text: str):
        """Pong!"""
        await cxt.bot.say("Pong! " + text)


def setup(bot):
    bot.add_cog(ButtonRoles(bot))
