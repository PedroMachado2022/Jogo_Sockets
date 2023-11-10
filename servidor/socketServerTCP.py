import socket
import threading
import random

HOST = "127.0.0.1"
PORT = 65432

salas = []

# Controle da sala
class Sala:
    def __init__(self, master_player):
        self.players = [master_player]
        self.cod_partida = None

    def create_code(self):
        self.cod_partida = random.randint(100000, 999999)

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def broadcast_message(self, message, sender):
        for player in self.players:
            if player != sender:
                try:
                    player.sendall(message.encode())
                except Exception as e:
                    print(f'Erro ao enviar mensagem para {player}: {e}')

                



# Conexão com o cliente
def handle_client(conn, addr):
    print(f"Connected by {addr}")
    
    while True:
        
        
        # Receber código da sala do cliente
        client_message = conn.recv(1024).decode().split(" ")

        print(client_message)

        if client_message[0] == 'Create_room':
            partida = Sala(conn)
            partida.create_code()
            conn.sendall(str(partida.cod_partida).encode())
            salas.append(partida)
        
        elif client_message[0] == 'Number_players':
            conn.sendall(str(partida.players).encode())

        elif client_message[0] == 'Find_room':

            sala_existente = next((sala for sala in salas if sala.cod_partida == int(client_message[1])), None)

            if sala_existente:
                sala_existente.add_player(conn)
                print(f"{addr} entrou na sala {sala_existente.cod_partida}")

                # Voltar quantos players estão na sala
                players_na_sala = len(sala_existente.players)
                conn.sendall(f'players {players_na_sala}'.encode())

                # Envia mensagem para todos os jogadores na sala informando sobre o novo jogador
                message = f"Jogador {addr} entrou na sala {sala_existente.cod_partida}"
                sala_existente.broadcast_message(message, addr)

        elif client_message[0] == ('Leave_room'):

            sala_associada = next((sala for sala in salas if conn in sala.players), None)

            if sala_associada:
                if conn in sala_associada.players:
                    sala_associada.players.remove(conn)

                    # Envia mensagem para todos os jogadores na sala informando sobre a saida do novo jogador
                    message = f"Jogador {addr} saiu da sala {sala_associada.cod_partida}"
                    sala_associada.broadcast_message(message, addr)
                    break

                else:
                    print(f"Erro: Jogador {addr} não está na sala {sala_associada.cod_partida}")
        
        elif client_message[0] == ('P'):
            sala_existente = next((sala for sala in salas if sala.cod_partida == int(client_message[1])), None)
            print(sala_existente.players)

        conn.sendall(str().encode())

    print(f"Connection closed by {addr}")
    conn.close()




# Servidor
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()


if __name__ == "__main__":
    main()
