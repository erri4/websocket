import json
import WebsocketServer as ws


response_headers: dict[str, int] = {
                                    'success': 1,
                                    'fail': 2,
                                    'name': 3,
                                    'xp': 4,
                                    'friend': 5,
                                    'rm_name': 6,
                                    'rm_ppl': 7,
                                    'sys': 8,
                                    'uate': 9,
                                    'rowcount': 10,
                                    'sql': 11,
                                    'sqlerr': 12,
                                    'pyres': 13,
                                    'rooms': 14,
                                    'move': 15,
                                    'ate': 16,
                                    'msg': 17
                                    }


class User:
    id: int = 0
    loginmode: int = 0
    # key:
    # 0: logged out
    # 1: logged in
    # 2: guest
    name = None
    room = None
    x: int = 0
    y: int = 0
    xp: int = 0
    friends: list[str] = []
    color: list[int] = [0, 0, 0]
    
    def __init__(self, client: ws.WebsocketServer.Client) -> None:
        """
        a class for managing the websocket connections as clients.

        <code>client: Client: </code> the websocket connection.
        """
        self.client: ws.WebsocketServer.Client = client


    def move(self, x: int, y: int) -> None:
        """
        change the position of the user.

        <code>x: integer: </code> the new x of the client.<br>
        <code>y: integer: </code> the new y of the client.

        <code>return: None. </code>
        """
        self.x = x
        self.y = y


    def set_name_color(self, name: str, color: list[int]) -> None:
        """
        change the name and color of the user.

        <code>name: string: </code> the new name of the client.<br>
        <code>color: list of integers: </code> the new rgb color of the client.

        <code>return: None. </code>
        """
        self.name = name
        self.color = color

    
    def send(self, msg: str | list | int, header: str) -> None:
        """
        send a message to the client.

        <code>msg: string | list | integer: </code> the message to send.<br>
        <code>header: string: </code> the header of the message.

        <code>return: none. </code>
        """
        if header == None:
            header = 'msg'
        self.client.send(json.dumps([response_headers[header], msg]))
