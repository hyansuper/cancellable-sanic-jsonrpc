from sanic_jsonrpc import SanicJsonrpc, _routing
from typing import Any, AnyStr, Callable, Dict, List, Optional, Tuple, Union
from sanic import Sanic
import random, sys, asyncio
from asyncio import CancelledError

class CancellableSanicJsonrpc(SanicJsonrpc):
    def __init__(
            self,
            app: Sanic,
            post_route: Optional[str] = None,
            ws_route: Optional[str] = None,
            *,
            access_log: bool = True
    ):
        SanicJsonrpc.__init__(self, app, post_route, ws_route, access_log=access_log)
        
        @self
        def _cancel_(task_name):
            for task in asyncio.all_tasks():
                if task.get_name() == str(task_name):
                    task.cancel()

    def cancellable(
            self,
            method_: Optional[str] = None,
            *,
            is_post_: Tuple[bool, ...] = (True, False),
            is_request_: Tuple[bool, ...] = (True, False),
            **annotations: type
    ) -> Callable:
        def cancellable_deco(coro):
            if not asyncio.iscoroutinefunction(coro):
                raise Exception(coro.__name__, 'must be a coroutine to be cancellable.')
            async def new_coro(*args, **kwargs):
                # set current task's name to the task id sent by client, so this task can be found and cancelled later.
                asyncio.current_task().set_name(str(args[-1]))
                return await coro(*args[len(args)//2:-1], **kwargs)                
            return new_coro

        cancellable_coro = cancellable_deco(method_)
        route = _routing.Route.from_inspect(cancellable_coro, method_.__name__, annotations)
        self._routes.update({(ip, ir, route.method): route for ip in is_post_ for ir in is_request_})
        return cancellable_coro



