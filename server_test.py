from sanic import Sanic
from cancellable_sanic_jsonrpc import CancellableSanicJsonrpc as SanicJsonrpc
import asyncio

app = Sanic('server')
jsonrpc = SanicJsonrpc(app, post_route='/api/rpc/post', ws_route='/api/rpc/ws')

@jsonrpc.cancellable
async def print4ever():
	while True:
		await asyncio.sleep(1)
		print('still running...')

@jsonrpc
async def cancel(task_name):
	for task in asyncio.Task.all_tasks():
		if task.get_name() == task_name:
			task.cancel()
			break

app.run(host='127.0.0.1', port=8000)