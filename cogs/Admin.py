from discord.ext import commands


class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role("Mod")
    async def delete(self, ctx, amount: int):
        """bulk deletes messages"""
        await ctx.channel.purge(limit=amount)


def setup(bot):
    bot.add_cog(Admin(bot))