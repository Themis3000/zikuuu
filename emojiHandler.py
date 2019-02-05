from dataHandler import find_message, get_button


def emoji_change(data):
    if find_message(data.d.message_id):
        return True
