import socket
import json

class ClienteTCP:
    def __init__(self, page):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sala = None
        self.players = 1
        self.page = page
        self.pecas = []
        self.sair_base = -1
        self.andar = []
        self.turno = 0
        self.vez_de_jogar = False
        
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
        message = 'Atualizar/'
        self.enviar_mensagem(message)
    
    def sair(self):
        message = 'Leave_room/'
        self.enviar_mensagem(message)
        self.sala = None

    

    def proximo_turno(self,txt, cont, dado=0):
        posicao = []
        # for i in pecas:
        #     posicao.append(i.posicao)
        # self.pecas = posicao
        self.enviar_mensagem(f'Next_turn/{txt}/{cont}/{dado}')
        

    def Encontrar_sala(self, sala):
        message = 'Find_room/' + sala
        self.enviar_mensagem(message)

    def Iniciar_jogo(self):
        message = 'Start_game/'
        self.enviar_mensagem(message)

    def Voltar_sala(self):
        return self.sala


    def receber_mensagens(self):
        while True:
            
            mensagem = self.sock.recv(1024).decode()
            print(mensagem)
            # Estrutura da mensagem funçao/dados de return/plus
            if mensagem:
                mensagem = mensagem.split('/')
                
                if mensagem[0] == "Players":
                    self.players = int(mensagem[1])
                    self.sala = int(mensagem[2])

                elif mensagem[0] == "Player_saiu":
                    self.atualizar()
                
                elif mensagem[0] == 'Iniciar_jogo':
                    self.page = 4
                
                elif mensagem[0] == 'Pode_jogar':
                    self.vez_de_jogar=True
                
                elif mensagem[0] == 'Att_Turno':
                    self.turno = int(mensagem[1])
                    print("degug turno", self.turno)

                elif mensagem[0] == 'Andar':
                    self.andar.append(int(mensagem[1]))
                    self.andar.append(int(mensagem[2]))
                    print('debug: Andou peca')
                elif mensagem[0] == 'Sair':
                    self.sair_base = int(mensagem[1])
                    print('debug: Saiu peca')