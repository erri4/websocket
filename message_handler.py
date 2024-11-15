from helper_funcs import pool, getcliby, getroomby, sendrooms, login, addname, sendparts, users, rooms
from classes.exceptions import UnrelatedException
from classes.Room import Room
import bcrypt
import websocket_server as ws
from typing import NoReturn


def message_handler(client: dict, server: ws.WebsocketServer, msg: str | list, header: str) -> None | NoReturn:
    """
    handle the message.

    <code>client: dictionary:</code> the client who sent a message.<br>
    <code>sever: WebsocketServer:</code> the websocket server.<br>
    <code>msg: string | list:</code> the message the client sent.<br>
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
    - <code>sql:</code> admin feature. run sql.
    - <code>py:</code> admin feature. run python.

    <code>return: None.</code>
    """
    global users
    global rooms
    c = getcliby('client', client)
    obj = users[c]
    r = None
    if obj.room != None:
        r = getroomby('name', obj.room)
    if header == 'login':
        if obj.name != None:
            raise UnrelatedException()
        if type(getcliby('name', msg[0])) != bool:
            raise UnrelatedException(2)
        ADMINHASH = b'$2b$12$4kuZ2dRYzCqpUR70spcFSeqgMgA4R92DK8San1MPer71YFudQ5ShC'
        if msg[0] == 'admin':
            if bcrypt.checkpw(msg[1].encode(), ADMINHASH):
                users[c].set_name_color(msg[0], [0, 0, 0])
                users[c].send(server, 'name', 'success')
            else:
                users[c].send(server, 'incorrect password', 'fail')
        else:
            l = login(str(msg[0]), msg[2])
            if l == True:
                users[c].set_name_color(msg[0], msg[1])
                users[c].send(server, 'name', 'success')
                users[c].send(server, msg[0], 'name')
                sql = f"select id, xp from users where username='{obj.name}'"
                with pool.select(sql) as s:
                    xp = s.sqlres[0]['xp']
                    users[c].send(server, xp, 'xp')
                    users[c].id = s.sqlres[0]['id']
                sql = f"select f_of from friends where friend='{obj.id}'"
                with pool.select(sql) as s:
                    for row in s.sqlres:
                        id = row['f_of']
                        sql = f"select username from users where id={id}"
                        with pool.select(sql) as se:
                            users[c].friends.append(se.sqlres[0]['username'])
                users[c].send(server, users[c].friends, 'friend')
                sendrooms(users[c], server)
                print(f'new client: {msg[0]}')
            else:
                users[c].send(server, l, 'fail')
    elif header == 'reg':
        if obj.name != None:
            raise UnrelatedException()
        if msg[0] != 'admin':
            if addname(str(msg[0]), msg[2]):
                users[c].set_name_color(msg[0], msg[1])
                users[c].send(server, 'name', 'success')
                users[c].send(server, msg[0], 'name')
                sendrooms(users[c], server)
                print(f'new client: {msg[0]}')
                sql = f"select id, xp from users where username='{obj.name}'"
                with pool.select(sql) as s:
                    xp = s.sqlres[0]['xp']
                    users[c].send(server, xp, 'xp')
                    users[c].id = s.sqlres[0]['id']
            else:
                users[c].send(server, 'username already exists', 'fail')
        else:
            users[c].send(server, 'username already exists', 'fail')
    elif header == 'create':
        if msg[0] == None:
            msg[0] = f"{obj.name}'s room"
        ex = getroomby('name', msg[0])
        if type(ex) == bool:
            ro = Room(str(msg[0]), obj, msg[1])
            rooms.append(ro)
            users[c].send(server, 'room', 'success')
            users[c].room = f'{msg[0]}'
            users[c].send(server, msg[0], 'rm_name')
            users[c].send(server, [[obj.name, True, True]], 'rm_ppl')
            for cl in users:
                if cl.room == None:
                    sendrooms(cl, server)
            ro.move(server)
            print(f'{obj.name} created room: {msg[0]}')
        else:
            users[c].send(server, 'room already exists', 'fail')
    elif header == 'join':
        rom = getroomby('name', msg[0])
        if type(rom) != bool:
            if users[c] not in rooms[rom].blacklist:
                if rooms[rom].password == None or msg[1] == rooms[rom].password:
                    rooms[rom].sysmsg(f'{obj.name} have joined the room', server)
                    rooms[rom].add_participant(users[c])
                    rooms[rom].move(server)
                    users[c].send(server, msg, 'rm_name')
                    users[c].send(server, 'room', 'success')
                    users[c].room = f'{msg[0]}'
                    for part in rooms[rom].participants:
                        sendparts(part, server)
                    print(f'{obj.name} joined room: {msg[0]}')
                else:
                    users[c].send(server, 'incorrect password', 'fail')
            else:
                users[c].send(server, 'you were banned from this room', 'fail')
    elif header == 'col':
        users[c].color = msg
        if type(r) != bool and r != None:
            rooms[r].move(server)
    elif header == 'leave':
        if r == None:
            raise UnrelatedException(1)
        rm = rooms[r].remove_participant(users[c])
        users[c].room = None
        rname = str(rooms[r].name)
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
        users[c].send(server, '', 'rm_name')
        users[c].send(server, '', 'rm_ppl')
        print(f'{obj.name} left room: {rname}')
    elif header == 'msg':
        if r == None:
            raise UnrelatedException(1)
        if msg[0] != '/':
            rooms[r].sendmsg(msg, users[c], server)
            print(f'{obj.name} send: {msg} in room: {rooms[r].name}')
        else:
            if users[c] == rooms[r].host:
                l = msg.strip().split(' ')
                l[0] = l[0][1:]
                if len(l) >= 2:
                    if l[0] == 'kick' and l[1] != obj.name:
                        k = getcliby('name', l[1])
                        if type(k) != bool and users[k] in rooms[r].participants:
                            rooms[r].remove_participant(users[k])
                            users[k].room = None
                            users[k].send(server, 'you were kicked from the room', 'sys')
                            users[k].send(server, '--disconnected from room--', 'sys')
                            rooms[r].sysmsg(f'{l[1]} was kicked from the room', server)
                            rooms[r].move(server)
                            for part in rooms[r].participants:
                                sendparts(part, server)
                            for cl in users:
                                    if cl.room == None:
                                        sendrooms(cl, server)
                            users[k].send(server, '', 'rm_name')
                            users[k].send(server, '', 'rm_ppl')
                    elif l[0] == 'ban' and l[1] != obj.name:
                        k = getcliby('name', l[1])
                        if type(k) != bool and users[k] in rooms[r].participants:
                            rooms[r].remove_participant(users[k])
                            rooms[r].blacklist.append(users[k])
                            users[k].room = None
                            users[k].send(server, 'you were banned from the room', 'sys')
                            users[k].send(server, '--disconnected from room--', 'sys')
                            rooms[r].sysmsg(f'{l[1]} was banned from the room', server)
                            rooms[r].move(server)
                            for part in rooms[r].participants:
                                sendparts(part, server)
                            for cl in users:
                                    if cl.room == None:
                                        sendrooms(cl, server)
                            users[k].send(server, '', 'rm_name')
                            users[k].send(server, '', 'rm_ppl')
                    elif l[0] == 'givehost':
                            k = getcliby('name', l[1])
                            if type(k) != bool:
                                rooms[r].host = users[k]
                                for part in rooms[r].participants:
                                    sendparts(part, server)
    elif header == 'move':
        users[c].move(msg[0], msg[1])
        rooms[r].move(server)
    elif header == 'eat':
        for part in rooms[r].participants:
            if msg[0] < int(part.x) + 29 and msg[0] > int(part.x) - 29:
                    if msg[1] < int(part.y) + 29 and msg[1] > int(part.y) - 29:
                        if part.client != client:
                            p = getcliby('client', part.client)
                            sql = f"select xp from users where username='{obj.name}'"
                            with pool.select(sql) as s:
                                xp = s.sqlres[0]['xp']
                                xp += 10
                                sql = f"update users set xp={xp} where username='{obj.name}'"
                                pool.runsql(sql)
                            users[p].move(0, 0)
                            part.send(server, '', 'uate')
                            users[c].send(server, xp, 'xp')
                            rep = [[obj.name, part.name], [[obj.color[0], obj.color[1], obj.color[2]], [part.color[0], part.color[1], part.color[2]]]]
                            rooms[r].sendall(rep, server, 'ate')
                            print(f'{obj.name} ate {part.name}')
        rooms[r].move(server)
    elif header == 'del':
        sql = f"delete from friends where friend='{obj.id}' or f_of='{obj.id}'"
        pool.runsql(sql)
        sql = f"delete from users where username='{obj.name}'"
        pool.runsql(sql)
    elif header == 'changep':
        sql = f"update users set pass='{msg}' where username='{obj.name}'"
        pool.runsql(sql)
    elif header == 'addf':
        sql = f"select id from users where username='{msg}'"
        with pool.select(sql) as se:
            if se.rowcount == 1:
                sql = f"select * from friends where friend={obj.id} and f_of={users[getcliby('name', msg)].id}"
                with pool.select(sql) as s:
                    if s.rowcount == 0:
                        sql = f"insert into friends values ({obj.id}, {users[getcliby('name', msg)].id})"
                        pool.runsql(sql)
                        sql = f"select * from friends where friend={obj.id}"
                        with pool.select(sql) as s:
                            for row in s.sqlres:
                                id = row['f_of']
                                sql = f"select username from users where id={id}"
                                with pool.select(sql) as se:
                                    users[c].friends.append(se.sqlres[0]['username'])
                        users[c].send(server, users[c].friends, 'friend')
    elif header == 'remf':
        sql = f"select id from users where username='{msg}'"
        with pool.select(sql) as se:
            if se.rowcount == 1:
                sql = f"select * from friends where friend={obj.id} and f_of={se.sqlres[0]['id']}"
                with pool.select(sql) as s:
                    if s.rowcount > 0:
                        sql = f"delete from friends where friend={obj.id} and f_of={se.sqlres[0]['id']}"
                        pool.runsql(sql)
                        users[c].friends.remove(msg)
                        users[c].send(server, users[c].friends, 'friend')
                        if users[c].room == None:
                            sendrooms(users[c], server)
                        else:
                            for part in rooms[r].participants:
                                sendparts(part, server)
    elif header == 'sql' and obj.name == 'admin':
        try:
            if msg.find('select') == -1:
                row = pool.runsql(msg)
                users[c].send(server, row, 'rowcount')
            else:
                r = []
                with pool.select(msg) as s:
                    r = [s.sqlres, s.rowcount]
                    users[c].send(server, r, 'pyres')
        except Exception as e:
            users[c].send(server, str(e), 'sqlerr')
    elif header == 'py' and obj.name == 'admin':
        try:
            output = eval(msg)
            users[c].send(server, str(output), 'pyres')
        except Exception as e:
            users[c].send(server, str(e), 'pyres')
