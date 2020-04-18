from sanic_jsonrpc import SanicJsonrpc, _routing
from typing import Any, AnyStr, Callable, Dict, List, Optional, Tuple, Union
from sanic import Sanic
import random, sys, asyncio

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

    def cancellable(
            self,
            method_: Optional[str] = None,
            *,
            is_post_: Tuple[bool, ...] = (True, False),
            is_request_: Tuple[bool, ...] = (True, False),
            **annotations: type
    ) -> Callable:
        def cancellable_deco(method):
            async def new_method(*args, **kwargs):
                msg_id = 1
                asyncio.Task.current_task().set_name(msg_id)
                await return method(*args, **kwargs)
            return new_method

        cancellable_method = cancellable_deco(method_)
        route = _routing.Route.from_inspect(cancellable_method, method_.__name__, annotations)
        self._routes.update({(ip, ir, route.method): route for ip in is_post_ for ir in is_request_})
        return cancellable_method



