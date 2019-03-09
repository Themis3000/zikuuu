from discord.ext import commands


class Allow:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role("Mod")
    async def allow(self, ctx, user):
        """Allow someone to join the text channel you are in one time only"""
        print(await commands.MemberConverter.convert(ctx=ctx, argument=user))
        await ctx.send(f"allowing {user}")


def setup(bot):
    bot.add_cog(Allow(bot))
