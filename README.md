# Projeto-web-chat
 - Eu criei este repositório para salvar os testes e aplicativos que eu criar relacionados a sockets e websockets.
 - Os arquivos estão separados por pastas.
 
 ## 1° Server Socket:
  Contém dois arquivos: 
   - server-socket.py: Um Client que se conecta a um servdor socket.
     
   - client-socket.py: Um Servidor de broadcast que recebe clientes através de uma conexão socket.

## 2° Server WebSocket:
 Contém quatro pastas:
  - Server:
    - server-websocket.py: Um servidor de broadcast que recebe clientes através de uma conexão websocket.
      - Bibliotecas Instaladas: websockets, asyncio, logging
  
  - client:
    -  client_websocket_consume: Um script que recebe as respostas de um servidor websocket.
    -  client_websocket_produce: Um script que envia mensagens a um servidor websocket.
       - Bibliotecas Instaladas: websockets, asyncio, logging
   
  - Client App:
    - app.py: Um programa com GUI que se conecta a um servidor websocket e permite enviar e receber mensagens.
    - display.py: Parte do programa "app.py" responsável pelo GUI.
       - Bibliotecas Instaladas: websockets, asyncio, pyqt5

  - Client App Teste:
    - app.py: Um programa com GUI que se conecta a um servidor websocket público e permite enviar e receber mensagens.
    - display.py: Parte do programa "app.py" responsável pelo GUI.
    - web_scraper_key.py: Script responsável por atualizar a key e gerar um novo link na inicialização do programa.
    - <a href="https://github.com/QueirozT/Projeto-web-chat/raw/main/Server%20WebSocket/Client%20App%20Teste/WebSocketsChat.exe" target="blank">WebSocketsChat.exe</a>: Um executável que foi compilado usando este programa como base.
       - Bibliotecas Instaladas: aiohttp, asyncio, beautifulsoup4, cryptocode, pyqt5, websockets
