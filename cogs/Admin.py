from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Admins")
    async def delete(self, ctx, amount: int):
        """bulk deletes messages"""
        await ctx.channel.purge(limit=amount+1)


def setup(bot):
    bot.add_cog(Admin(bot))
