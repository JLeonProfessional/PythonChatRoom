import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 55555

nickname = input("Choose a nickname: ")
client.connect((host, port))

def receive():
    while True:
        # try:
        message = client.recv(1024).decode('ascii')
        if message == "NICK":
            client.send(nickname.encode('ascii'))
        else:
            print(message)
        # except:
        #     print("an error occurred!")
        #     client.close()
        #     break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()


