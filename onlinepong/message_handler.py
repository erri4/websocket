from helper_funcs import getcliby, users
from typing import NoReturn
import classes.WebsocketServer as ws


def message_handler(client: ws.WebsocketServer.Client, msg: str | list | int, header: str) -> None | NoReturn:
    """
    handle the message.

    <code>return: None. </code>
    """
    global users
    c = getcliby('client', client)
    obj = users[c]
    if header == 'name':
        users[c].name = msg
        if len(users) < 2:
            users[c].active = True
        print(f'new client: {msg}')
    elif header == 'move':
        users[c].move(msg)
        users[c].send(msg, 'you')
        other = getcliby('active', True, obj.name, 'name')
        users[other].send(msg, 'move')
    else:
        raise ValueError('invalid header')
