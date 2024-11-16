import classes.websocketserver as ws
import json
from classes.User import User
import message_handler
from helper_funcs import sendrooms, getroomby, sendparts, getcliby, users, rooms
from classes.exceptions import UnrelatedException


def new_client(client: ws.WebsocketServer.Client) -> None:
    """
    new client setup. creating an instace of user and appending it to the users list.

    <code>client: Client: </code> the new client.<br>
    <code>sever: WebsocketServer: </code> the websocket server.

    <code>return: None. </code>
    """
    cl = User(client)
    users.append(cl)


def client_left(client: ws.WebsocketServer.Client) -> None:
    """
    client left setup. removing the client from users list and room if it was inside a room.

    <code>client: Client: </code> the client who left.<br>
    <code>sever: WebsocketServer: </code> the websocket server.

    <code>return: None. </code>
    """
    c = getcliby('client', client)
    obj = users[c]
    if obj.room != None:
        room = obj.room
        r = getroomby('name', room)
        rm = rooms[r].remove_participant(users[c])
        users[c].room = None
        if rm == False:
            rooms[r].sysmsg(f'{obj.name} have left the room')
            rooms[r].move()
            for part in rooms[r].participants:
                sendparts(part)
        else:
            del rooms[r]
        for cl in users:
            if cl.room == None:
                sendrooms(cl)
    del users[c]
    if obj.name != 'admin' and obj.name != None:
        print(f'client left: {obj.name}')


def message_received(client: ws.WebsocketServer.Client, msg: str) -> None:
    """
    parse the message and call message_handler function.

    <code>client: Client: </code> the client who sent a message.<br>
    <code>sever: WebsocketServer: </code> the websocket server.<br>
    <code>msg: string: </code> the message the client sent.

    <code>return: None. </code>
    """
    msg = json.loads(msg)
    header = msg[0]
    msg = msg[1]
    try:
        message_handler.message_handler(client, msg, header)
    except UnrelatedException as e:
        print(e.errtxt)

def start_server() -> None:
    """
    start the websocket server.
    """
    server = ws.WebsocketServer(host=f'0.0.0.0', port=5001)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    
    print(f'Server listening on port 5001')
    server.start()
