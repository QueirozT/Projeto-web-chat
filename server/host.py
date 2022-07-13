import socket
import threading

# Informações do Servidor
host = ''
port = 55555

# Iniciando o Servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server.bind((host, port))
server.listen()

# Lista de Clients e Nicknames
clients = []
nicknames = []


# Função de broadcast para enviar mensagens para todos os clientes
def broadcast(message):
    for client in clients:
        client.send(message)


# Função de tratamento de mensagens
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(2048)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('utf-8'))
            print(f'{nickname} disconnected')
            nicknames.remove(nickname)
            break


# Recebendo / Listando as Funções
def receive():
    while True:
        # Aceitando a conexão
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Solicitando e Recebendo o Nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(2048).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Mostrando para todos o novo usuário
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        # Iniciando o novo processo de tratamento de mensagens para o cliente em uma thread
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# Chamando a função para inicializar o servidor
receive()
