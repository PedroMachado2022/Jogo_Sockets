import socket
import threading
import random

HOST = "127.0.0.1"
PORT = 65432

salas = []
lock = threading.Lock()

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

    def enviar_mensagem_broadcast(self, mensagem, remetente):
        for player in self.players:
            if player != remetente:
                try:
                    player.sendall(mensagem.encode())
                except Exception as e:
                    print(f'Erro ao enviar mensagem para {player}: {e}')

def handle_client(conn, addr):
    print(f"Conectado por {addr}")
    sala_associada = None

    try:
        while True:
            client_message = conn.recv(1024).decode().split(" ")

            if not client_message:
                break

            if client_message[0] == 'Create_room':
                print(f"Cliente: {addr} -- abriu conexao com sala")
                sala_associada = Sala(conn)
                sala_associada.criar_codigo()
                conn.sendall(str(sala_associada.cod_partida).encode())
                salas.append(sala_associada)

            elif client_message[0] == 'Number_players':
                conn.sendall(str(sala_associada.players).encode())

            elif client_message[0] == 'Find_room':
                sala_existente = next((sala for sala in salas if sala.cod_partida == int(client_message[1])), None)
                if sala_existente:
                    sala_existente.adicionar_jogador(conn)
                    print(f"{addr} entrou na sala {sala_existente.cod_partida}")
                    players_na_sala = len(sala_existente.players)
                    conn.sendall(f'players {players_na_sala}'.encode())
                    mensagem = f"Jogador {addr} entrou na sala {sala_existente.cod_partida}"
                    sala_existente.enviar_mensagem_broadcast(mensagem, addr)

            elif client_message[0] == ('Leave_room'):
                if sala_associada:
                    if conn in sala_associada.players:
                        sala_associada.remover_jogador(conn)
                        mensagem = f"Jogador {addr} saiu da sala {sala_associada.cod_partida}"
                        sala_associada.enviar_mensagem_broadcast(mensagem, addr)
                        if not sala_associada.players:
                            salas.remove(sala_associada)
                            sala_associada = None

            elif client_message[0] == ('P'):
                sala_existente = next((sala for sala in salas if sala.cod_partida == int(client_message[1])), None)
                print(sala_existente.players)

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
