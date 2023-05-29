import json
import socket
import threading
import time
import datetime
from StringHelper import encode, decode

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 55558

username = input("Username: ")
password = input("Password: ")


nickname = ""
client.connect((host, port))

login_map = {
            "username": username,
            "password": password
        }
login_json = json.dumps(login_map)

client.sendall(bytes(login_json,encoding="utf-8"))


def receive():
    global nickname
    while True:
        try:
            message = decode(client.recv(1024))
            if message == "NICK":
                nickname = input("Enter nickname: ")
                client.send(encode(nickname))
            else:
                print(message)
        except:
            print("an error occurred!")
            client.close()
            break


def write():
    while True:
        message_map = {
            "name": nickname,
            "time": time.time(),
            "message": f'{input("")}',
        }
        message_json = json.dumps(message_map)

        client.sendall(bytes(message_json,encoding="utf-8"))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()


