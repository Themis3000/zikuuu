from discord.ext import commands


class Admin:
    def __init__(self, bot):
        self.bot = bot

# todo:Themi figure out how to make the bot throw a syntax error in chat when ANY command it done wrong without doing a try for each. End goal: I can add commands without even thinking about making a syntax error out, it will do that for me

    @commands.command(pass_context=True)
    @commands.has_role("Mod")
    async def delete(self, ctx, amountstr: str):
        """bulk deletes messages"""
        try:
            amountint = int(amountstr)+1
        except:
            await ctx.send('Syntax error: argument 1 is not a number. use: !delete {Num to delete}')
        else:
            await ctx.channel.purge(limit=amountint)


def setup(bot):
    bot.add_cog(Admin(bot))
