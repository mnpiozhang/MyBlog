#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from channels.routing import route
from blogweb.consumers import ws_message,ws_connect,ws_disconnect


channel_routing = [
    #route("http.request", "backend.consumers.http_consumer"),
    #route("websocket.receive", ws_message),
    route("websocket.connect", ws_connect, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route("websocket.receive", ws_message, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route("websocket.disconnect", ws_disconnect, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
]