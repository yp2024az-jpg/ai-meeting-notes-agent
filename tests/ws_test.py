import asyncio
import json
import websockets

async def run():
    uri='ws://127.0.0.1:8000/ws/transcript'
    try:
        async with websockets.connect(uri)as ws:
            await ws.send(json.dumps({'type':'transcript','text':'Hello from automated test','timestamp':'2026-01-03T00:00:00Z'}))
            msg = await ws.recv()
            print('Received:', msg)
    except Exception as e:
        print('WS test error:', e)

if __name__ == '__main__':
    asyncio.run(run())
