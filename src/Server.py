import json
import threading
import socket
import datetime
from mongo_setup import *
from DataService import *
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
    received_message = decode(message)
    message_data = json.loads(received_message)
    message_contents = message_data["message"]
    if message_contents.startswith('!'):
        message_contents = handle_command(message_contents)
    timestamp = datetime.datetime.fromtimestamp(message_data["time"])
    datetime_string = timestamp.strftime("%Y-%m-%d %H:%M")
    return f'[{datetime_string}] {message_data["name"]}: {message_contents}'


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

        login_info = decode(client.recv(1024))
        login_data = json.loads(login_info)
        username = login_data["username"]
        password = login_data["password"]
        create_user(username, password)
        print(f"{username}, {password}")

        print(f"Connected with {str(address)}")

        nickname = request_client_information(client)

        print(f'Nickname of the client is {nickname}')

        broadcast(encode(f'{nickname} joined the chat'))

        client.send(encode(f'Connected to the server!'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening")
receive()

