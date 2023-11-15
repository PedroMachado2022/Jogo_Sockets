import socket

class ClienteTCP:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sala = None
        self.players = 1

        
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
        message = 'Players'
        self.enviar_mensagem(message)


    def criar_sala(self):
        message = 'Create_room'
        self.enviar_mensagem(message)

    
    def Encontrar_sala(self, sala):
        message = 'Find_room ' + sala
        self.enviar_mensagem(message)


    def Voltar_sala(self):
        return self.sala


    def receber_mensagens(self):
        while True:
            
            mensagem = self.sock.recv(1024).decode()
            print(mensagem)
            # Estrutura da mensagem funçao/dados de return/plus
            if mensagem:
                mensagem = mensagem.split(' ')
                if mensagem[0] == "ReturnSala":
                    self.sala = mensagem[1]

                elif mensagem[0] == "Players":
                    self.players = mensagem[1]

                elif mensagem[0] == "Player_saiu":
                    self.atualizar()