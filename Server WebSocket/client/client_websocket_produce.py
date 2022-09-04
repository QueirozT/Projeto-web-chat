import asyncio
import websockets
from websockets import WebSocketClientProtocol


# PRODUCER
async def produce(nickName: str, url: str) -> None:
    async with websockets.connect(url) as ws:
        while True:
            await ws.send(f"{nickName}: {input('Sua Mensagem: ')}")
            await ws.recv()


if __name__ == "__main__":
    websocket_resource_url = "ws://localhost:55555"

    nickName = input("Digite seu nick: ")

    try:
        asyncio.run(produce(nickName, websocket_resource_url))
    except ConnectionRefusedError:
        print("\nConnection refused\n")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt\n")
        exit()
    except:
        print("\nUnknown error\n")
        exit()
