'''
Script responsavel pela comunicação com o servidor, Enviar mensagem, receber msg e tratar msg
'''

import socket

# Objeto com intuito de fazer a comunicaçao com o servidor
class ClienteTCP:
    def __init__(self, page):
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sala = None
        self.players = 1
        self.page = page
        self.sair_base = -1
        self.andar = []
        self.turno = 0
        self.vez_de_jogar = False
        self.mensagens = ['Digite textos']
    
    # Estabelece a comunicação com o servidor
    def conectar(self, host, port):
        self.sock.connect((host, port))

    # Função padrão para envio de mensagens para servidor
    def enviar_mensagem(self, msg):
        print(msg)
        try:
            self.sock.sendall(msg.encode())
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")

    # Funçao pra enviar mensagem 
    def Enviar_msg_chat(self, msg):
        
        try:
            self.sock.sendall(f'Chat/{msg}'.encode())
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")

    # Atualizar informaçoes de sala caso entre ou saia um player
    def atualizar(self):
        message = 'Atualizar/'
        self.enviar_mensagem(message)
    
    # Avisar caso o player saia 
    def sair(self):
        message = 'Leave_room/'
        self.enviar_mensagem(message)
        self.sala = None

    # Atualizar informações do turno para outro players
    def proximo_turno(self,txt, cont=None, dado=0):
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

    #Função para ficar recenbendo informaçoes do servidor
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

                elif mensagem[0] == "Chat":
                    if len(self.mensagens) > 9:
                        self.mensagens.pop(0)
                    self.mensagens.append(mensagem[1])
                elif mensagem[0] == 'Sair':
                    self.sair_base = int(mensagem[1])
                    print('debug: Saiu peca')