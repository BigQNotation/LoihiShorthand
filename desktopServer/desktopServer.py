import asyncio
import pathlib
import ssl
import websockets
import os

async def get_File(websocket, path):
	async for sentData in websocket:
		name = await websocket.recv()
		dirname = os.path.dirname(__file__)
		wfile = open(dirname+"/storage/"+ name)
		while feed = ws.recv_frame():
			wfile.write(feed.data)
		print"Transfer Complete"

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_cert_chain(localhost_pem)

start_server = websockets.serve(get_File, "localhost", 9999, ssl=ssl_context)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()