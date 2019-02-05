import pickledb

db = pickledb.load('./buttondata.json', False)


def add_buttons(messageid, array):
    db.set(messageid, array)
    db.dump()


def find_message(messageid):
    return db.exists(messageid)


def get_button(messageid, button):
    message_data = db.get(messageid)
    return message_data[1][message_data[0].index(button)]

