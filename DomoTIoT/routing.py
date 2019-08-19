from channels import include
from channels import route
from .consumers import *

channel_routing = [
	include("web.routing.websocket_routing",path=r'^/web'),
]

websocket_routing = [
	route("websocket.connect", ws_add),
	route("websocket.receive", ws_message),
	route("websocket.disconnect", ws_disconnect),
]
