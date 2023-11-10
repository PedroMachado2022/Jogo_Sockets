import socket
import threading

HOST = "127.0.0.1"
PORT = 65432

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

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        # O cliente escolhe ou recebe um código de sala
        codigo_sala = input("Enter the room code: ")
        s.sendall(codigo_sala.encode())

        receive_thread = threading.Thread(target=receive_messages, args=(s,))
        receive_thread.start()

        send_thread = threading.Thread(target=send_messages, args=(s,))
        send_thread.start()

        receive_thread.join()
        send_thread.join()

if __name__ == "__main__":
    main()
