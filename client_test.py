from asyncio import get_event_loop, sleep
from aiohttp import ClientSession
import random, sys

async def main():
    url = 'http://127.0.0.1:8000/api/rpc'
    task_id = random.randint(0, sys.maxsize)
    # to issue a cancellable jsonrpc request, an unique task id must be placed at last of 'params' field.
    # print 10 times on server side unless cancelled
    print_request = {'jsonrpc': '2.0', 'method': 'print_task', 'params':[10, task_id], 'id': 1}
    # to cancel a previous task, make a jsonrpc request with 'method' field as '_cancel_', and the previous task id as 'params'.
    cancel_request = {'jsonrpc': '2.0', 'method': '_cancel_', 'params':[task_id], 'id': 2}
    async with ClientSession() as session:
        async with session.ws_connect(url) as ws:
            await ws.send_json(print_request)
            await sleep(5)
            await ws.send_json(cancel_request)
            print(await ws.receive_json())

if __name__ == '__main__':
    get_event_loop().run_until_complete(main())
