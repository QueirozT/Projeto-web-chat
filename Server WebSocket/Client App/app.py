import sys, asyncio, websockets, time
from threading import Thread
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QListWidgetItem
from PyQt5.QtCore import Qt, QTime
from display import *


class Chat(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        # Inicialização de Variáveis
        self.stackedWidget.setCurrentWidget(self.pgLogin)
        self.listChat.clear()
        self.listChat.setWordWrap(True)
        self.listChat.setSpacing(5)
        self.url = "ws://localhost:55555"
        self.nick = ""

        # Inputs e Botões
        self.btnEntrar.clicked.connect(self.join_chat)
        self.btnEnviar.clicked.connect(self.send_msg)
        self.inputMsg.returnPressed.connect(self.send_msg)
        self.inputNick.returnPressed.connect(self.join_chat)

        # Chamando o método Copiar Mensagem para o item da lista
        self.listChat.itemDoubleClicked.connect(self.msg_copy)


    # Copiar Mensagem
    def msg_copy(self, lstItem):
        text = lstItem.text().split('\n')
        text = ''.join(text[1])
        self.inputMsg.setText(text)
        self.inputMsg.selectAll()
        self.inputMsg.copy()
        self.inputMsg.setText('')


    # Método que inicia o Chat e as Threads
    def join_chat(self):
        if self.inputNick.text():
            self.nick = self.inputNick.text()
            self.stackedWidget.setCurrentWidget(self.pgChat)
                
            # Iniciando Uma Thread para Receber Mensagens
            self.RecThread = ReceiveThread(self.url, self.listChat, self.nick)
            self.RecThread.daemon = True  # para que o thread feche quando o programa acabar
            self.RecThread.start() # inicia o thread

            # Iniciando Uma Thread para Enviar Mensagens
            self.MSG = ''
            self.sendThread = SendThread(self.url, self.MSG)
            self.sendThread.daemon = True  # para que o thread feche quando o programa acabar
            self.sendThread.start() # inicia o thread


    # Método que envia a Mensagem
    def send_msg(self):
        # Mostrando Mensagem Enviada
        self.msg = self.inputMsg.text()
        item = QListWidgetItem(f"{self.nick} - {QTime.currentTime().toString('H:m')}\n{self.msg}")
        item.setBackground(Qt.green)
        item.setTextAlignment(Qt.AlignRight)
        self.listChat.addItem(item)
        self.inputMsg.setText('')

        # Enviando Mensagem para o Thread de Envio
        self.sendThread.msg = f"{self.nick} - {QTime.currentTime().toString('H:m')}\n{self.msg}"



class SendThread(Thread):
    def __init__(self, url, msg):
        self.url = url
        self.msg = msg
        super().__init__()


    # Inicializador do Thread, Chamando o Produce
    def run(self):
        asyncio.run(self.produce())


    # Método para Enviar Mensagens
    async def produce(self) -> None:
        async for ws in websockets.connect(self.url):
            try: 
                tempo = round(time.time())
                while tempo + 40 > round(time.time()):
                    if self.msg:
                        await ws.send(self.msg)
                        await ws.recv()
                        self.msg = ''
                        time.sleep(1)
            except websockets.ConnectionClosed:
                continue



class ReceiveThread(Thread):
    def __init__(self, url, listChat, nick):
        self.url = url
        self.listChat = listChat
        self.nick = nick
 
        super().__init__()  # Chamando o inicializador da thread
 

    # Inicializador do Thread, Chamando o Consume
    def run(self):
        asyncio.run(self.consume(self.url))
            

    # Método para Receber Mensagens
    async def consume(self, url: str) -> None:
        async for ws in websockets.connect(self.url):
                async for msg in ws:
                    try:
                        if not self.nick == msg[:len(self.nick)]:
                            item = QListWidgetItem(msg)
                            item.setBackground(Qt.gray)
                            item.setTextAlignment(Qt.AlignLeft)
                            self.listChat.addItem(item)
                    except websockets.ConnectionClosed:
                        continue



if __name__ == "__main__":
    app = QApplication([])

    # Definindo a janela
    window = Chat()

    # Iniciando o programa
    window.show()
    app.exec_()

    # Saindo do programa
    sys.exit()
