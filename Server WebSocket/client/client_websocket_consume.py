import asyncio
import logging
import websockets
from websockets import WebSocketClientProtocol


# CONSUMER
logging.basicConfig(level=logging.INFO)


async def consumer_handler(websocket: WebSocketClientProtocol) -> None:
    async for message in websocket:
        log_message(message)


async def consume(url) -> None:
    async with websockets.connect(url) as websocket:
        await consumer_handler(websocket)


def log_message(message: str) -> None:
    logging.info(f"\n\tMessage:{message}\n")
    # print(message)  # Mensagem recebida



if __name__ == "__main__":
    websocket_resource_url = f"ws://localhost:55555"

    try:
        ## INICIALIZAÇÃO ATRAVÉS DE asyncio.run
        asyncio.run(consume(websocket_resource_url))
        
        ## INICIALIZAÇÃO ATRAVÉS DE LOOP
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(consume(websocket_resource_url))
        # loop.run_forever()
    except ConnectionRefusedError:
        print("\nConnection refused\n")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt\n")
        exit()
