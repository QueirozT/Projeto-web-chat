import asyncio, logging, websockets, pathlib
from websockets import WebSocketServerProtocol
# ## IMPORTS PARA USAR NO HEROKU
# import os
# import signal


### LOG SALVO EM ARQUIVO ###
# path = pathlib.Path(__file__).parent
# logging.basicConfig(
#     filename=f'{pathlib.Path.joinpath(path, "server_websockets.log")}',
#     filemode='w',
#     encoding='utf-8',
#     format='%(levelname)s : %(asctime)s >>> %(message)s',
#     datefmt='%m/%d/%Y %I:%M:%S %p',
#     level=logging.INFO
# )

### LOG EXIBIDO NO CONSOLE ###
path = pathlib.Path(__file__).parent
logging.basicConfig(
    format='%(levelname)s : %(asctime)s >>> %(message)s',
    datefmt='%m/%d/%y %I:%M:%S %p',
    level=logging.INFO
)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects.')

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects.')

    async def send_to_clients(self, message: str) -> None:
        if self.clients:
            # Use wait or gather
            await asyncio.gather(*[client.send(message) for client in self.clients])

    async def ws_handler(self, ws: WebSocketServerProtocol) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        except websockets.ConnectionClosedError:
            pass
        except Exception as e:
            logging.warning(e.__class__)
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            await self.send_to_clients(message)


async def main():
    server = Server()
    port = 55555
    async with websockets.serve(server.ws_handler, "", port) as server_coro:
        await server_coro.wait_closed()


# # ## MAIN PARA USAR NO HEROKU
# async def main():
#     # Set the stop condition when receiving SIGTERM.
#     server = Server()
#     loop = asyncio.get_running_loop()
#     stop = loop.create_future()
#     loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

#     port = int(os.environ.get("PORT", "55555"))
#     async with websockets.serve(server.ws_handler, "", port):
#         await stop


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer Stoped!\n")
        exit()
