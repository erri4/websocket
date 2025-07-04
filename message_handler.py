from helper_funcs import getcliby, getroomby, sendrooms, login, addname, sendparts, namexists, initfriends, users, rooms, pool
from classes.exceptions import UnrelatedException
from classes.Room import Room
import bcrypt
from typing import Never
import WebsocketServer as ws


REQUEST_HEADERS: dict[int, str] = {
                                    0: 'login',
                                    1: 'reg',
                                    2: 'create',
                                    3: 'join',
                                    4: 'col',
                                    5: 'leave',
                                    6: 'msg',
                                    7: 'move',
                                    8: 'eat',
                                    9: 'del',
                                    10: 'changep',
                                    11: 'addf',
                                    12: 'remf',
                                    13: 'sql',
                                    14: 'py',
                                    15: 'gue'
                                    }


def message_handler(client: ws.Client, msg: str | list | int, header: str) -> None | Never:
    """
    handle the message.

    <code>client: Client:</code> the client who sent a message.<br>
    <code>msg: string | list | integer:</code> the message the client sent.<br>
    <code>header: string:</code> the header of the message the client sent.<br>
    valid headers:<br>
    - <code>login:</code> log in.
    - <code>reg:</code> register.
    - <code>create:</code> create a room.
    - <code>join:</code> join a room.
    - <code>col:</code> change the color.
    - <code>leave:</code> leave room.
    - <code>msg:</code> send message in the room.
    - <code>move:</code> move the avatar in the game.
    - <code>eat:</code> eat someone in the game.
    - <code>del:</code> delete the account.
    - <code>changep:</code> change the password.
    - <code>addf:</code> add a friend.
    - <code>remf:</code> remove a friend.
    - <code>sql:</code> admin feature. runs sql.
    - <code>py:</code> admin feature. runs python.

    <code>return: None.</code>
    """
    global users
    global rooms
    header = REQUEST_HEADERS[header]

    c = getcliby('client', client)
    c: int
    obj = users[c]
    r = getroomby('name', obj.room)
    if header == 'login':
        if obj.name != None:
            raise UnrelatedException()
        if getcliby('name', msg[0]) != None:
            raise UnrelatedException(2)
        ADMINHASH = b'$2b$12$4kuZ2dRYzCqpUR70spcFSeqgMgA4R92DK8San1MPer71YFudQ5ShC'
        if msg[0] == 'admin':
            if bcrypt.checkpw(msg[1].encode(), ADMINHASH):
                users[c].set_name_color(msg[0], [0, 0, 0])
                users[c].send('name', 'success')
                users[c].loginmode = 1
            else:
                users[c].send('incorrect password', 'fail')
        else:
            l = login(str(msg[0]), msg[2])
            if l == True:
                users[c].set_name_color(msg[0], msg[1])
                users[c].send('name', 'success')
                users[c].send(msg[0], 'name')
                sql = f"select id, xp from users where username='{obj.name}'"
                with pool.select(sql) as s:
                    xp = s.sqlres.get(row=0, column='xp')
                    users[c].send(xp, 'xp')
                    users[c].id = s.sqlres.get(row=0, column='id')
                    users[c].xp = xp
                initfriends(users[c])
                sendrooms(users[c])
                print(f'new client: {msg[0]}')
                users[c].loginmode = 1
            else:
                users[c].send(l, 'fail')
    elif header == 'reg':
        if obj.name != None:
            raise UnrelatedException()
        if msg[0] != 'admin' and addname(str(msg[0]), msg[2]):
            users[c].set_name_color(msg[0], msg[1])
            users[c].send('name', 'success')
            users[c].send(msg[0], 'name')
            sendrooms(users[c])
            print(f'new client: {msg[0]}')
            sql = f"select id from users where username='{obj.name}'"
            with pool.select(sql) as s:
                users[c].send(0, 'xp')
                users[c].id = s.sqlres.get(row=0, column='id')
            users[c].loginmode = 1
        else:
            users[c].send('username already exists', 'fail')
    elif header == 'gue':
        if obj.name != None:
            raise UnrelatedException()
        if msg[0] != 'admin' and not namexists(msg[0]):
            users[c].set_name_color(msg[0], msg[1])
            users[c].send(['name', True], 'success')
            users[c].send(msg[0], 'name')
            sendrooms(users[c])
            print(f'new client: {msg[0]}')
            users[c].send(0, 'xp')
            users[c].loginmode = 2
        else:
            users[c].send('username already exists', 'fail')
    elif header == 'create':
        if msg[0] == None:
            msg[0] = f"{obj.name}'s room"
        ex = getroomby('name', msg[0])
        if ex == None:
            ex: int
            ro = Room(str(msg[0]), obj, msg[1])
            rooms.append(ro)
            users[c].send('room', 'success')
            users[c].room = f'{msg[0]}'
            users[c].send(msg[0], 'rm_name')
            users[c].send([[obj.name, True, True]], 'rm_ppl')
            for cl in users:
                if cl.room == None and cl.name != None:
                    sendrooms(cl)
            ro.move()
            print(f'{obj.name} created room: {msg[0]}')
        else:
            users[c].send('room already exists', 'fail')
    elif header == 'join':
        rom = getroomby('name', msg[0])
        if rom != None:
            rom: int
            if users[c] not in rooms[rom].blacklist:
                if rooms[rom].password == None or msg[1] == rooms[rom].password:
                    rooms[rom].sysmsg(f'{obj.name} have joined the room')
                    rooms[rom].add_participant(users[c])
                    rooms[rom].move()
                    users[c].send(msg[0], 'rm_name')
                    users[c].send('room', 'success')
                    users[c].room = f'{msg[0]}'
                    for part in rooms[rom].participants:
                        sendparts(part)
                    print(f'{obj.name} joined room: {msg[0]}')
                else:
                    users[c].send('incorrect password', 'fail')
            else:
                users[c].send('you were banned from this room', 'fail')
    elif header == 'col':
        users[c].color = msg
        if r != None:
            r: int
            rooms[r].move()
    elif header == 'leave':
        if type(r) == bool:
            raise UnrelatedException(1)
        rm = rooms[r].remove_participant(users[c])
        users[c].room = None
        rname = str(rooms[r].name)
        if rm == False:
            rooms[r].sysmsg(f'{obj.name} have left the room')
            rooms[r].move()
            for part in rooms[r].participants:
                sendparts(part)
        else:
            del rooms[r]
        for cl in users:
                if cl.room == None and cl.name != None:
                    sendrooms(cl)
        users[c].send('', 'rm_name')
        users[c].send('', 'rm_ppl')
        print(f'{obj.name} left room: {rname}')
    elif header == 'msg':
        if r == None:
            raise UnrelatedException(1)
        r: int
        if msg[0] != '/':
            rooms[r].sendmsg(msg, users[c])
            print(f'{obj.name} sent {msg} in room {rooms[r].name}')
        else:
            if users[c] == rooms[r].host:
                l = msg.strip().split(' ')
                l[0] = l[0][1:]
                if len(l) >= 2:
                    if l[0] == 'kick' and l[1] != obj.name:
                        k = getcliby('name', l[1])
                        if k != None and users[k] in rooms[r].participants:
                            k: int
                            rooms[r].remove_participant(users[k])
                            users[k].room = None
                            users[k].send('you were kicked from the room', 'sys')
                            users[k].send('--disconnected from room--', 'sys')
                            rooms[r].sysmsg(f'{l[1]} was kicked from the room')
                            rooms[r].move()
                            for part in rooms[r].participants:
                                sendparts(part)
                            for cl in users:
                                    if cl.room == None and cl.name != None:
                                        sendrooms(cl)
                            users[k].send('', 'rm_name')
                            users[k].send('', 'rm_ppl')
                    elif l[0] == 'ban' and l[1] != obj.name:
                        k = getcliby('name', l[1])
                        if k != None and users[k] in rooms[r].participants:
                            k: int
                            rooms[r].remove_participant(users[k])
                            rooms[r].blacklist.append(users[k])
                            users[k].room = None
                            users[k].send('you were banned from the room', 'sys')
                            users[k].send('--disconnected from room--', 'sys')
                            rooms[r].sysmsg(f'{l[1]} was banned from the room')
                            rooms[r].move()
                            for part in rooms[r].participants:
                                sendparts(part)
                            for cl in users:
                                    if cl.room == None:
                                        sendrooms(cl)
                            users[k].send('', 'rm_name')
                            users[k].send('', 'rm_ppl')
                    elif l[0] == 'givehost':
                            k = getcliby('name', l[1])
                            if k != None:
                                k: int
                                rooms[r].host = users[k]
                                for part in rooms[r].participants:
                                    sendparts(part)
    elif header == 'move':
        users[c].move(msg[0], msg[1])
        rooms[r].move()
    elif header == 'eat':
        for part in rooms[r].participants:
            if obj.x < int(part.x) + 29 and obj.x > int(part.x) - 29:
                    if obj.y < int(part.y) + 29 and obj.y > int(part.y) - 29:
                        if part.client != client:
                            if obj.loginmode == 1:
                                sql = f"select xp from users where username='{obj.name}'"
                                with pool.select(sql) as s:
                                    xp = s.sqlres.get(row=0, column='xp')
                                    xp += 10
                                    sql = f"update users set xp={xp} where username='{obj.name}'"
                                    pool.runsql(sql)
                            xp = obj.xp
                            xp += 10
                            p = getcliby('client', part.client)
                            p: int
                            users[p].move(0, 0)
                            part.send('', 'uate')
                            users[c].send(xp, 'xp')
                            rep = [[obj.name, part.name], [[obj.color[0], obj.color[1], obj.color[2]], [part.color[0], part.color[1], part.color[2]]]]
                            rooms[r].sendall(rep, 'ate')
                            print(f'{obj.name} ate {part.name}')
        rooms[r].move()
    elif header == 'del':
        if obj.loginmode == 1:
            sql = f"delete from friends where friend='{obj.id}' or f_of='{obj.id}'"
            pool.runsql(sql)
            sql = f"delete from users where username='{obj.name}'"
            pool.runsql(sql)
    elif header == 'changep':
        if obj.loginmode == 1:
            sql = f"update users set pass='{msg}' where username='{obj.name}'"
            pool.runsql(sql)
    elif header == 'addf':
        f: int = getcliby('name', msg)
        if obj.loginmode == 1 and users[f].loginmode == 1:
            sql = f"select id from users where username='{msg}'"
            with pool.select(sql) as se:
                if se.rowcount == 1:
                    sql = f"select * from friends where friend={obj.id} and f_of={users[f].id}"
                    with pool.select(sql) as s:
                        if s.rowcount == 0:
                            sql = f"insert into friends values ({obj.id}, {users[f].id})"
                            pool.runsql(sql)
                            initfriends(users[c])
                            sendparts(users[c])
    elif header == 'remf':
        f: int = getcliby('name', msg)
        if obj.loginmode == 1 and users[f].loginmode == 1:
            sql = f"select id from users where username='{msg}'"
            with pool.select(sql) as se:
                if se.rowcount == 1:
                    sql = f"select * from friends where friend={obj.id} and f_of={se.sqlres.get(row=0, column='id')}"
                    with pool.select(sql) as s:
                        if s.rowcount > 0:
                            sql = f"delete from friends where friend={obj.id} and f_of={se.sqlres.get(row=0, column='id')}"
                            pool.runsql(sql)
                            initfriends(users[c])
    elif header == 'sql' and obj.name == 'admin':
        try:
            if msg.find('select') == -1:
                row = pool.runsql(msg)
                users[c].send(row, 'rowcount')
            else:
                r = []
                with pool.select(msg) as s:
                    r = [s.sqlres.data, s.rowcount]
                    users[c].send(r, 'sql')
        except Exception as e:
            users[c].send(str(e), 'sqlerr')
    elif header == 'py' and obj.name == 'admin':
        try:
            output = eval(msg)
            users[c].send(str(output), 'pyres')
        except Exception as e:
            users[c].send(str(e), 'pyres')
    else:
        raise ValueError('invalid header')