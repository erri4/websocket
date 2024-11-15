import json
import websocket_server as ws
    

class User:
    """
    a class for managing the websocket connections as clients.
    """
    id: int = 0
    name = None
    room = None
    x: int = 0
    y: int = 0
    friends: list[str] = []
    color: list[int] = [0, 0, 0]
    
    def __init__(self, client: dict) -> None:
        """
        store the websocket connection.

        <code>client: dictionary:</code> the websocket connection.

        <code>return: None.</code>
        """
        self.client: dict = client


    def move(self, x: int, y: int) -> None:
        """
        change the position of the user.

        <code>x: integer:</code> the new x of the client.<br>
        <code>y: integer:</code> the new y of the client.

        <code>return: None.</code>
        """
        self.x = x
        self.y = y


    def set_name_color(self, name: str, color: list[int]) -> None:
        """
        change the name and color of the user.

        <code>name: string:</code> the new name of the client.<br>
        <code>color: list of integers:</code> the new rgb color of the client.

        <code>return: None.</code>
        """
        self.name = name
        self.color = color

    
    def send(self, server: ws.WebsocketServer, msg: str | list, header: str) -> None:
        """
        send a message to the client.

        <code>server: WebsocketServer:</code> the server to send the message with.<br>
        <code>msg: string | list:</code> the message to send.<br>
        <code>header: string:</code> the header of the message.

        <code>return: none.</code>
        """
        if header == None:
            header = 'msg'
        server.send_message(self.client, json.dumps([header, msg]))
