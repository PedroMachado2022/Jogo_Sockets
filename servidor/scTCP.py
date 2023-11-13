import socket

class ClienteTCP:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players = []


        
    def conectar(self, host, port):
        self.sock.connect((host, port))

    def receber_mensagens(self):
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(f"Recebido do servidor: {data.decode()}")

    def enviar_mensagem(self, msg):
        try:
            self.sock.sendall(msg.encode())
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")

    def atualizar(self):
        message = 'Number_players'
        self.enviar_mensagem(message)

        data = self.sock.recv(1024)
        print(f"Recebido do servidor: {data.decode()}")
        return data.decode()

    def criar_sala(self):
        message = 'Create_room'
        self.enviar_mensagem(message)

        data = self.sock.recv(1024)
        return data.decode()