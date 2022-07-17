import aiohttp
import asyncio
from bs4 import BeautifulSoup
import cryptocode

import websockets

URL = 'https://www.piesocket.com/websocket-tester'
KEY = ''


async def fetch():
  global URL
  global KEY

  async with aiohttp.ClientSession() as session:
    async with session.get(URL) as response:
      resp = await response.text()
      html = BeautifulSoup(resp, 'html.parser')
      KEY = html.select_one('.sm\:px-6:nth-child(2) .sm\:col-span-2').get_text()
      

def coletar_key():
  asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  asyncio.run(fetch())
  
  return KEY.strip()


def gerar_link():
  key = coletar_key()

  url = f'wss://demo.piesocket.com/v3/channel_10?api_key={key}&notify_self'

  return url

if __name__ == '__main__':
  # BASE: wss://demo.piesocket.com/v3/channel_10?api_key=VCXCEuvhGcBDP7XhiJJUDvR1e1D3eiVjgZ9VRiaV&notify_self

  # print(coletar_key())
  "wss://demo.piesocket.com/v3/channel_10?api_key=VCXCEuvhGcBDP7XhiJJUDvR1e1D3eiVjgZ9VRiaV&notify_self"

  
  print(gerar_link())

  msg = 'Mensagem de Teste'
  code = 'aVoaVpl2mvEUMrcWkym+9gdXD3bTDbH4cXQs7G9OfRpwVMRJScqQ2Ch1qK1WzXB6jQ'
  mensagem = cryptocode.encrypt(msg, code)
  print("MENSAGEM ENCRYPTADA: ",mensagem)
  print("MENSAGEM DECRYPTADA: ", cryptocode.decrypt(mensagem, code))
