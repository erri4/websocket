import json
import websocket_server as ws
    

class User:
    id: int = 0
    name = None
    room = None
    x: int = 0
    y: int = 0
    friends: list[str] = []
    
    def __init__(self, client: dict) -> None:
        self.client: dict = client


    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


    def set_name_color(self, name: str, color: list[int]) -> None:
        self.name = name
        self.color: list[int] = color

    
    def send(self, server: ws.WebsocketServer, msg: str | list, header: str) -> None:
        if header == None:
            header = 'msg'
        server.send_message(self.client, json.dumps([header, msg]))
