from discord.ext import commands
import discord
import asyncio
from utils.checks import in_channel


class Allow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Admins")
    async def allow(self, ctx, member: discord.Member):
        """Allow someone to join the voice channel you are in one time only"""
        channel = ctx.author.voice.channel
        await channel.set_permissions(member, connect=True, speak=True)
        await ctx.send(f"`allowed {member} to join {channel.name} for the next 10 seconds`")
        # todo:Themi This try statement is very gross, when msg is a success it falls under an except saying: 'bool' object is not callable. Although is dosen't cause any problems this looks and feels gross
        try:
            msg = await self.bot.wait_for('voice_state_update', check=in_channel(member, channel), timeout=10)
            await channel.set_permissions(member, overwrite=None)
        except asyncio.TimeoutError:
            await channel.set_permissions(member, overwrite=None)
        except Exception as e:
            print(f"except: {e}")
            await channel.set_permissions(member, overwrite=None)
        else:
            pass


def setup(bot):
    bot.add_cog(Allow(bot))
