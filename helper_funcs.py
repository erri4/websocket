import classes.database as db
import websocket_server as ws
import classes.User as User
import classes.Room as Room


users: list[User.User] = []
rooms: list[Room.Room] = []
HOST: str = 'localhost'
USER: str = 'root'
PASSWORD: str = '033850900reefmysql'
DATABASE: str = 'mysqldb'
PORT: int = 3300
pool = db.ConnectionPool(HOST, USER, PASSWORD, DATABASE, PORT)


def getcliby(attr: str, con) -> (int | bool):
    global users
    for i in range(len(users)):
        if getattr(users[i], attr) == con:
            return i
    return False


def getroomby(attr: str, con) -> (int | bool):
    global rooms
    for i in range(len(rooms)):
        if getattr(rooms[i], attr) == con:
            return i
    return False


def login(name: str, p: str) -> (bool | str):
    sql = f"select pass from users where username='{name}'"
    with pool.select(sql) as s:
        if s.rowcount == 1:
            pa = s.sqlres[0]['pass']
            if pa == p:
                return True
            return 'incorrect password'
        return 'user does not exist'


def addname(name: str, passw: str) -> bool:
    sql = f"select username from users where username='{name}'"
    with pool.select(sql) as s:
        if not s.rowcount > 0:
            sql = f"insert into users (username, pass, xp) values ('{name}', '{passw}', 0)"
            pool.runsql(sql)
            return True
        return False
    

def sendrooms(clobj: User.User, server: ws.WebsocketServer) -> None:
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
    global rooms
    rom = getroomby('name', clobj.room)
    parts = rooms[rom].participants
    re = []
    for p in parts:
        re.append([p.name, p.name in clobj.friends or p.name == clobj.name, p == rooms[rom].host])
    clobj.send(server, re, 'rm_ppl')
