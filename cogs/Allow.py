from discord.ext import commands
import discord
import asyncio
from utils.checks import in_channel


class Allow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def allow(self, ctx, member: discord.Member):
        """Allow someone to join the voice channel you are in one time only (must have role "Admins")"""
        channel = ctx.author.voice.channel
        if ctx.author.voice:
            await channel.set_permissions(member, connect=True, speak=True)
            await ctx.send(f"allowing `{member}` to join `{channel.name}` one time only for the next 500 seconds")
            # todo:Themi This try statement is very gross, when msg is a success it falls under an except saying: 'bool' object is not callable. Although is dosen't cause any problems this looks and feels gross
            try:
                msg = await self.bot.wait_for('voice_state_update', check=in_channel(member, channel), timeout=500)
                await channel.set_permissions(member, overwrite=None)
            except asyncio.TimeoutError:
                await channel.set_permissions(member, overwrite=None)
            except Exception:
                await channel.set_permissions(member, overwrite=None)
            else:
                pass
        else:
            ctx.send(f"@{ctx.author} You are not in a voice channel")


def setup(bot):
    bot.add_cog(Allow(bot))
