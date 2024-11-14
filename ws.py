import websocket_server as ws
import json
from classes.User import User
import message_handler
from helper_funcs import sendrooms, getroomby, sendparts, getcliby, users, rooms


def new_client(client: dict, server: ws.WebsocketServer) -> None:
    cl = User(client)
    users.append(cl)


def client_left(client: dict, server: ws.WebsocketServer) -> None:
    c = getcliby('client', client)
    obj = users[c]
    if obj.room != None:
        room = obj.room
        r = getroomby('name', room)
        rm = rooms[r].remove_participant(users[c])
        users[c].room = None
        if rm == False:
            rooms[r].sysmsg(f'{obj.name} have left the room', server)
            rooms[r].move(server)
            for part in rooms[r].participants:
                sendparts(part, server)
        else:
            del rooms[r]
        for cl in users:
            if cl.room == None:
                sendrooms(cl, server)
    del users[c]
    if obj.name != 'admin' and obj.name != None:
        print(f'client left: {obj.name}')


def message_received(client: dict, server: ws.WebsocketServer, msg: str) -> None:
    msg = json.loads(msg)
    header = msg[0]
    msg = msg[1]
    message_handler.message_handler(client, server, msg, header)

def start_server(ip) -> None:
    server = ws.WebsocketServer(host=f'{ip}', port=5001)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    
    print(f'Server listening on {ip}:5001')
    server.run_forever(threaded=True)
