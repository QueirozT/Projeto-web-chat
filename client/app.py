import socket
import threading

# Escolhendo um Nickname
nick = input("\nChoose your nickname: ")

# Conectando ao Servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))


# Escutando o servidor e enviando o Nickname
def receive():
    while True:
        try:
            # Recebe a mensagem do servidor
            # Se for 'NICK' Envia o Nickname
            message = client.recv(2048).decode('utf-8')
            if message == 'NICK':
                client.send(nick.encode('utf-8'))
            else:
                print(message)
        except:
            # Fechando a conexão com o servidor
            print("An error occured!")
            client.close()
            break


# Enviando mensagens para o servidor
def write():
    while True:
        message = '{}: {}'.format(nick, input(''))
        client.send(message.encode('utf-8'))


# Chamando as funções de escuta e envio em threads para funcionarem simultaneamente
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
