import classes.database as db
import websocket_server as ws
import classes.User as User
import classes.Room as Room
from typing import Any


users: list[User.User] = []
rooms: list[Room.Room] = []
HOST: str = 'localhost'
USER: str = 'root'
PASSWORD: str = '033850900reefmysql'
DATABASE: str = 'mysqldb'
PORT: int = 3300
pool = db.ConnectionPool(HOST, USER, PASSWORD, DATABASE, PORT)


def getcliby(attr: str, con: Any) -> (int | bool):
    """
    gets a client location in the users list by an attribute.

    <code>attr: string:</code> the attribute to find the client by.<br>
    <code>con: any:</code> the content of the attribute.

    <code>return: integer | boolean:</code> the location of the client in the users list. false if it is not in the list.
    """
    global users
    for i in range(len(users)):
        if getattr(users[i], attr) == con:
            return i
    return False


def getroomby(attr: str, con: Any) -> (int | bool):
    """
    gets a room location in the rooms list by an attribute.

    <code>attr: string: the attribute to find the room by.<br>
    <code>con: any:</code> the content of the attribute.

    <code>return: integer | boolean:</code> the location of the room in the rooms list. false if it is not in the list.
    """
    global rooms
    for i in range(len(rooms)):
        if getattr(rooms[i], attr) == con:
            return i
    return False


def login(name: str, p: str) -> (bool | str):
    """
    tries to login with a given name and password. returns the fail details as a string if somethng failed.

    <code>name: string:</code> the name of the new account.<br>
    <code>p: string:</code> the password of the new account.

    <code>return: boolean | string:</code> returns what failed as a string. true if nothing failed.
    """
    sql = f"select pass from users where username='{name}'"
    with pool.select(sql) as s:
        if s.rowcount == 1:
            pa = s.sqlres[0]['pass']
            if pa == p:
                return True
            return 'incorrect password'
        return 'user does not exist'


def addname(name: str, passw: str) -> bool:
    """
    tries to register with a new account. returns false if account already exists.

    <code>name: string:</code> the name of the new account.<br>
    <code>passw: string:</code> the password of the new account.

    <code>return: boolean:</code> returns false if account already exist, and true if the process of registering was successful.
    """
    sql = f"select username from users where username='{name}'"
    with pool.select(sql) as s:
        if not s.rowcount > 0:
            sql = f"insert into users (username, pass, xp) values ('{name}', '{passw}', 0)"
            pool.runsql(sql)
            return True
        return False


def sendrooms(clobj: User.User, server: ws.WebsocketServer) -> None:
    """
    send the rooms available to a given client.

    <code>clobj: User:</code> the user the rooms are sent to.<br>
    <code>server: WebsocketServer:</code> the server the rooms are sent with.

    <code>return: None.</code>
    """
    global rooms
    roms = []
    for i in range(len(rooms)):
        finroom = []
        for part in rooms[i].participants:
            if part.name in clobj.friends:
                finroom.append(part.name)
        roms.append([rooms[i].name, finroom, rooms[i].password != None])
    clobj.send(server, roms, 'rooms')


def sendparts(clobj: User.User, server: ws.WebsocketServer) -> None:
    """
    send participants in the room for a given client.

    <code>clobj: User:</code> the user the participants are sent to.<br>
    <code>server: WebsocketServer:</code> the server the participants are sent with.

    <code>return: None.</code>
    """
    global rooms
    rom = getroomby('name', clobj.room)
    parts = rooms[rom].participants
    re = []
    for p in parts:
        re.append([p.name, p.name in clobj.friends or p.name == clobj.name, p == rooms[rom].host])
    clobj.send(server, re, 'rm_ppl')
