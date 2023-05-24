import socket
import threading
from StringHelper import encode, decode

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 55558

nickname = input("Choose a nickname: ")
client.connect((host, port))


def receive():
    while True:
        try:
            message = decode(client.recv(1024))
            if message == "NICK":
                client.send(encode(nickname))
            else:
                print(message)
        except:
            print("an error occurred!")
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(encode(message))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()


