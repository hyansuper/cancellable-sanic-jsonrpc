from sanic import Sanic
from cancellable_sanic_jsonrpc import CancellableSanicJsonrpc as SanicJsonrpc
import asyncio

app = Sanic('server')
jsonrpc = SanicJsonrpc(app, post_route='/api/rpc', ws_route='/api/rpc')

@jsonrpc.cancellable
# must be a coroutnine to be cancellable
async def print_task(count):
    while count>0:
        count -= 1
        await asyncio.sleep(1)
        print('still printing...', count)
    return 'done'

@jsonrpc
async def print_once():
    print('print once')
    return 'done'

app.run(host='127.0.0.1', port=8000)
