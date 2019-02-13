from discord.ext import commands
import asyncio


class Allow:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def allow(self, ctx, user='none'):
        """Allow someone to join the text channel you are in one time only"""
        if user != 'none':
            await commands.MemberConverter.convert(self=commands.Bot, ctx=ctx, argument=user)
            await ctx.send(f"allowing {user}")
        else:
            await ctx.send(f"You did not specify a user, do +allow (user)")


def setup(bot):
    bot.add_cog(Allow(bot))
