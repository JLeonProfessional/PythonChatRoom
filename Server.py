import threading
import socket

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


clients = []
nicknames = []


def handleCommand(message):
    message_elements = message.split(' ', 1)
    command = message_elements[0]
    if command.lower().startswith('!upper'):
        return message_elements[1].upper()
    else:
        return message


def broadcastSentMessage(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            string_message = message.decode('ascii')
            message_elements = string_message.split(': ', 1)
            message_contents = message_elements[1]
            print(message_contents)
            if message_contents.startswith('!'):
                message_contents = handleCommand(message_contents)
                message_elements[1] = message_contents
            string_message = f'{message_elements[0]}: {message_elements[1]}'
            broadcastSentMessage(string_message.encode('ascii'), client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat'.encode('ascii'))
        client.send(f'Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening")
receive()

