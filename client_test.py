from asyncio import get_event_loop, sleep

from aiohttp import ClientSession

async def main():
    url = 'http://127.0.0.1:8000/api/rpc'
    print_request = {'jsonrpc': '2.0', 'method': 'print4ever', 'params':[], 'id': 1}
    cancel_request = {'jsonrpc': '2.0', 'method': 'cancel', 'params':[0], 'id': 1}
    async with ClientSession() as session:
        async with session.ws_connect(url + '/ws') as ws:
            await ws.send_json(print_request)
            await sleep(5)
            await ws.send_json(cancel_request)
            #response = await ws.receive_json()
            #print(response['result'])

if __name__ == '__main__':
    get_event_loop().run_until_complete(main())