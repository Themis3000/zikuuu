import discord
from discord.ext import commands
from vars import TOKEN
from rawReceiveHandler import to_object
from emojiHandler import emoji_change
from dataHandler import add_buttons, get_button


client = commands.Bot(command_prefix='+')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    arguments = message.content.split(" ")
    if message.content.startswith('+test'):
        print('here')
        await client.add_reaction(message, '✅')
    if message.content.startswith('+ping'):
        await client.send_message(message.channel, 'Pong!')
    if message.content.startswith('+buttonarray'):
        if message.author.server_permissions.administrator:
            array = message.content[13:].split(', ')
            if len(array) % 2 == 0:
                await client.send_message(message.channel, 'The next message you send will have the functioning buttons')
                msg = await client.wait_for_message(author=message.author)
                buttons = [[], []]
                add_react = []
                for i in range(int(len(array) / 2)):
                    # emoji
                    buttons[0].append(array[i * 2])
                    if "<:" in buttons[0][len(buttons[0]) - 1]:
                        add_react.append(buttons[0][len(buttons[0]) - 1][2:][:-1])
                        buttons[0][len(buttons[0]) - 1] = buttons[0][len(buttons[0]) - 1][2:].split(":")[0]
                    else:
                        add_react.append(array[i * 2])
                    # role
                    buttons[1].append(array[i * 2 + 1])
                print(add_react)
                for i in add_react:
                    await client.add_reaction(msg, i)
                add_buttons(msg.id, buttons)
            else:
                await client.send_message(message.channel, 'Incorrect amount of parameters')


@client.event
async def on_socket_raw_receive(msg):
    try:
        data = to_object(msg)
        msg_type = data.t
    except:
        pass
    else:
        if msg_type == 'MESSAGE_REACTION_ADD' or data.t == 'MESSAGE_REACTION_REMOVE':
            if emoji_change(data):
                role = get_button(data.d.message_id, data.d.emoji.name)
                if msg_type == 'MESSAGE_REACTION_ADD':
                    await client.add_roles(client.get_server(data.d.guild_id).get_member(data.d.user_id), discord.utils.get(client.get_server(data.d.guild_id).roles, name=role))
                if msg_type == 'MESSAGE_REACTION_REMOVE':
                    await client.remove_roles(client.get_server(data.d.guild_id).get_member(data.d.user_id), discord.utils.get(client.get_server(data.d.guild_id).roles, name=role))


client.run(TOKEN)
