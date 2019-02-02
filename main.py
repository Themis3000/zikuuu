import discord
from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix='+')

client.get_message('react', 493252326186811394)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('+ping'):
        await client.send_message(message.channel, 'Pong!')


@client.event
async def on_reaction_add(reaction, user):
    print(user + 'reacted with: ' + reaction.emoji + ' on message: ' + reaction.message)


client.run('NDA5MTEyOTQwMjg5OTgyNDg0.DoiFpQ.LEyAli-K1dBVo9vVCChzx4ibOqQ')
