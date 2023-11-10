import socket
import threading

HOST = "127.0.0.1"
PORT = 65432

sock = None
players = []

def receive_messages(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print(f"Received from server: {data.decode()}")

def send_messages(sock):
    while True:
        message = input("Enter a message: ")
        sock.sendall(message.encode())

def Atualizar(sock):
    message = 'Number_players'
    sock.sendall(message.encode())

    data = sock.recv(1024)
    print(f"Received from server: {data.decode()}")
    return data.decode()

def Criar_sala(sock):
    message = 'Create_room'
    sock.sendall(message.encode())

    data = sock.recv(1024)
    return data.decode()

def main():
    global sock
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        sock = s
        # O cliente escolhe ou recebe um código de sala
        codigo_sala = input("Enter the room code: ")
        s.sendall(codigo_sala.encode())

        


if __name__ == "__main__":
        main()
