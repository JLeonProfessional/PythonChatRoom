import threading
import socket
from StringHelper import *

host = '127.0.0.1'
port = 55558

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


clients = []
nicknames = []


def handle_exception(client):
    index = clients.index(client)
    clients.remove(client)
    client.close()
    nickname = nicknames[index]
    broadcast(encode(f'{nickname} left the chat!'))
    nicknames.remove(nickname)


def request_client_information(client):
    client.send(encode("NICK"))
    nickname = decode(client.recv(1024))
    nicknames.append(nickname)
    clients.append(client)
    return nickname


def receive_message(client):
    message = client.recv(1024)
    string_message = decode(message)
    message_elements = string_message.split(': ', 1)
    message_contents = message_elements[1]
    print(message_contents)
    if message_contents.startswith('!'):
        message_contents = handle_command(message_contents)
        message_elements[1] = message_contents
    return f'{message_elements[0]}: {message_elements[1]}'


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
            string_message = receive_message(client)
            print(string_message)
            broadcastSentMessage(encode(string_message), client)
        except:
            handle_exception(client)
            break


def receive():
    while True:
        client, address = server.accept()

        print(f"Connected with {str(address)}")

        nickname = request_client_information(client)

        print(f'Nickname of the client is {nickname}')

        broadcast(encode(f'{nickname} joined the chat'))

        client.send(encode(f'Connected to the server!'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening")
receive()

