import sys, asyncio, websockets, time
from threading import Thread
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QListWidgetItem, QScrollBar, QAbstractItemView
from PyQt5.QtCore import Qt, QTime
from display import *


class Chat(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)


        # Inicialização de Variáveis
        self.url = "ws://localhost:55555"
        self.nick = ""

        self.stackedWidget.setCurrentWidget(self.pgLogin)

        self.listChat.clear()
        self.listChat.setWordWrap(True)
        self.listChat.setSpacing(5)
        
        self.listChat.model().rowsInserted.connect(lambda: self.listChat.scrollToBottom())

        scroll_bar = QScrollBar(self)
        scroll_bar.setStyleSheet("background: lightgreen; border: none; width: 0px;")
        self.listChat.setVerticalScrollBar(scroll_bar)
        self.listChat.setStyleSheet("""
            QListWidget::item {
                border-radius: 10px;
                padding: 5px;
                background: lightgray;
                width: 100%;
            }
        """)
        

        # Inputs e Botões
        self.btnEntrar.clicked.connect(self.join_chat)
        self.btnEnviar.clicked.connect(self.send_msg)
        self.inputMsg.returnPressed.connect(self.send_msg)
        self.inputNick.returnPressed.connect(self.join_chat)


        # Chamando o método Copiar Mensagem para o item da lista
        self.listChat.itemDoubleClicked.connect(self.msg_copy)


    # Método Copiar Mensagem
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
        ### Registrando a mensagem  ###
        self.msg = self.inputMsg.text()
        self.inputMsg.setText('')

        message = f"{self.nick} - {QTime.currentTime().toString('H:m')}\n{self.msg}"

        ### Enviando a Mensagem para o Thread de Envio  ###
        self.sendThread.msg = message

        ### Prévia da mensagem enviada... ###
        # obj = QListWidgetItem(message)
        # obj.setBackground(Qt.green)
        # obj.setTextAlignment(Qt.AlignRight)
        # self.listChat.addItem(obj)
        


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
            while True:
                try:
                    # Criando um check state para manter o socket aberto
                    await ws.send("PING")
                    await ws.recv()
                    await asyncio.sleep(0.2)

                    tempo = round(time.time())

                    while tempo + 30 > round(time.time()):
                        if self.msg:
                            await ws.send(self.msg)
                            await ws.recv()
                            self.msg = ''
                            await asyncio.sleep(0.2)
                except websockets.ConnectionClosed:
                    # print('Conexão perdida no Thread de Envio')
                    break



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
            try:
                async for msg in ws:
                    if msg != 'PING':
                        if not self.nick == msg[:len(self.nick)]:
                            obj = QListWidgetItem(msg)
                            obj.setBackground(Qt.gray)
                            obj.setTextAlignment(Qt.AlignLeft)
                            self.listChat.addItem(obj)
                        else:
                            obj = QListWidgetItem(msg)
                            obj.setBackground(Qt.green)
                            obj.setTextAlignment(Qt.AlignRight)
                            self.listChat.addItem(obj)
            except websockets.ConnectionClosed:
                # print('Conexão perdida no Thread de Recebimento')
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
