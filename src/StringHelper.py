def encode(message):
    return message.encode()


def decode(message):
    return message.decode()


def handle_command(message):
    message_elements = message.split(' ', 1)
    command = message_elements[0].lower()
    if command.startswith('!upper'):
        return change_to_upper(message_elements[1])
    else:
        return message


def change_to_upper(message):
    return message.upper()
