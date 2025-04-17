import DBConnectionPool as db
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


def getcliby(attr: str, con: Any) -> (int | None):
    """
    gets a client location in the users list by an attribute.

    <code>attr: string: </code> the attribute to find the client by.<br>
    <code>con: any: </code> the content of the attribute.

    <code>return: integer | none: </code> the location of the client in the users list. false if it is not in the list.
    """
    global users
    for i in range(len(users)):
        if getattr(users[i], attr) == con:
            return i


def getroomby(attr: str, con: Any) -> (int | None):
    """
    gets a room location in the rooms list by an attribute.

    <code>attr: string: the attribute to find the room by.<br>
    <code>con: any: </code> the content of the attribute.

    <code>return: integer | none: </code> the location of the room in the rooms list. false if it is not in the list.
    """
    global rooms
    for i in range(len(rooms)):
        if getattr(rooms[i], attr) == con:
            return i


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


def namexists(name: str) -> bool:
    """
    check if a user with specific username exists.

    <code>name: string:</code> the username to check existance of.

    <code>return: boolean:</code> returns false if the name is already taken, and true otherwise.
    """
    sql = f"select username from users where username='{name}'"
    with pool.select(sql) as s:
        if not s.rowcount > 0:
            return False
        return True


def addname(name: str, passw: str) -> bool:
    """
    tries to register with a new account. returns false if account already exists.

    <code>name: string:</code> the name of the new account.<br>
    <code>passw: string:</code> the password of the new account.

    <code>return: boolean:</code> returns false if account already exist, and true if the process of registering was successful.
    """
    if not namexists(name):
        sql = f"insert into users (username, pass, xp) values ('{name}', '{passw}', 0)"
        pool.runsql(sql)
        return True
    return False


def sendrooms(clobj: User.User) -> None:
    """
    send the rooms available to a given client.

    <code>clobj: User: </code> the user the rooms are sent to.

    <code>return: None. </code>
    """
    global rooms
    roms = []
    for i in range(len(rooms)):
        finroom = []
        for part in rooms[i].participants:
            if part.name in clobj.friends:
                finroom.append(part.name)
        roms.append([rooms[i].name, finroom, rooms[i].password != None])
    clobj.send(roms, 'rooms')


def sendparts(clobj: User.User) -> None:
    """
    send participants in the room for a given client.

    <code>clobj: User: </code> the user the participants are sent to.

    <code>return: None. </code>
    """
    global rooms
    rom = getroomby('name', clobj.room)
    parts = rooms[rom].participants
    re = []
    for p in parts:
        re.append([p.name, p.name in clobj.friends or p.name == clobj.name or p.loginmode == 2 or clobj.loginmode == 2, p == rooms[rom].host])
    clobj.send(re, 'rm_ppl')


def initfriends(user: User.User):
        user.friends = []
        sql = f"select f_of from friends where friend={user.id}"
        with pool.select(sql) as s:
            for row in s.sqlres:
                id = row['f_of']
                sql = f"select username from users where id={id}"
                with pool.select(sql) as se:
                    user.friends.append(se.sqlres[0]['username'])
        user.send(user.friends, 'friend')
