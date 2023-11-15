import socket
import threading
import random

HOST = "127.0.0.1"
PORT = 65432

salas = []
lock = threading.Lock()

# Criação de sala
class Sala:
    def __init__(self, master_player):
        self.players = [master_player]
        self.cod_partida = None

    def criar_codigo(self):
        self.cod_partida = random.randint(100000, 999999)

    def adicionar_jogador(self, jogador):
        self.players.append(jogador)

    def remover_jogador(self, jogador):
        self.players.remove(jogador)
        print('Jogador removido:')

    #Enviar mensagem para todos
    def enviar_mensagem_broadcast(self, mensagem, remetente):
        for player in self.players:
            if player != remetente:
                try:
                    player.sendall(mensagem.encode())
                except Exception as e:
                    print(f'Erro ao enviar mensagem para {player}: {e}')

#Conexao com player
def handle_client(conn, addr):
    print(f"Conectado por {addr}")
    sala_associada = None

    try:
        while True:
            
            #Estrutura da mensagem Funcao/variaveis/plus
            client_message = conn.recv(1024).decode().split(" ")

            if not client_message:
                break

            if client_message[0] == 'Create_room':
                #Debug
                print(f"Cliente: {conn} -- abriu conexao com sala")

                #Criar objeto sala
                sala_associada =  Sala(conn)
                sala_associada.criar_codigo()

                #Controle para saber se sala existe.
                salas.append(sala_associada)


            elif client_message[0] == 'Atualizar':
                #atualizar dados de sala
                if sala_associada:
                    conn.sendall(f'Players {len(sala_associada.players)} {sala_associada.cod_partida}'.encode())
                else:
                    conn.sendall(f'Players 0'.encode())


            elif client_message[0] == 'Find_room':
                
                #Verifica se sala existe 
                sala_associada = next((sala for sala in salas if sala.cod_partida == int(client_message[1])), None)

                if sala_associada:
                    sala_associada.adicionar_jogador(conn)
                    players_na_sala = len(sala_associada.players)
                    msg = f'Players {players_na_sala} {sala_associada.cod_partida}'
                    conn.sendall(msg.encode())
                    
                    sala_associada.enviar_mensagem_broadcast(msg, conn)
                    

            elif client_message[0] == ('Leave_room'):
                print(sala_associada.players)
                #Verifica sala
                if sala_associada:
                    
                    if conn in sala_associada.players:

                        sala_associada.remover_jogador(conn)
                        mensagem = f"Player_saiu {sala_associada.cod_partida}"

                        sala_associada.enviar_mensagem_broadcast(mensagem, conn)
                        #Verifica se tem alguem na sala ainda, se não existe apaga sala.
                        if not sala_associada.players:
                            print(f'sala removida: {sala_associada.cod_partida}')
                            salas.remove(sala_associada)
                            sala_associada = None



    except Exception as e:
        print(f"Erro durante a comunicação com {addr}: {e}")
    finally:
        print(f"Conexão encerrada por {addr}")
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"Servidor ouvindo em {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    main()