from utils.options import check_current
import os
import discord
from discord.ext import commands

# todo:Themi figure out a better help format method, send help to users dm.

# todo:Themi Fix code inconsistencies

client = commands.Bot(command_prefix=check_current("prefix"), status=discord.Status(check_current("status_booting")), activity=discord.Game(name=check_current("game_booting")))

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")


@client.event
async def on_ready():
    print("Ready to rumble")
    await client.change_presence(status=discord.Status(check_current("status")), activity=discord.Game(name=check_current("game")))

# todo:Themi Move all of this to a new file
# todo:Themi fix this absolute mess of code
# todo:Themi add more on command errors


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have the required perms to use that command")
    elif isinstance(error, commands.MissingRequiredArgument):
        await send_cmd_help(ctx)
    elif isinstance(error, commands.BadArgument):
        await send_cmd_help(ctx)
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{ctx.author.mention} You are using that command too often, chill out there buddyo. You can use that command {error.cooldown.rate} times per {int(error.cooldown.per)} seconds, and you can use it next in {round(error.retry_after, 2)} seconds")


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = await client.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        await ctx.send("Missing an argument, use: `" + pages[0].split("\n")[1] + "`")
    else:
        pages = await client.formatter.format_help_for(ctx, ctx.command)
        await ctx.send("Incorrect argument type, use: `" + pages[0].split("\n")[1] + "`")


client.run(os.environ["TOKEN"])

# non urgent to do starts here

# todo:Themi allow repo manager to reload cogs
# todo:Themi make a chat log system better then audit log
