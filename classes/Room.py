from User import User
import websocket_server as ws
from types import NoneType


class Room:
    blacklist: list[User] = []

    def __init__(self, name: str, creator: User, password: str | NoneType) -> None:
        self.name = name
        self.participants: list[User] = [creator]
        self.host: User = creator
        self.password = password


    def add_participant(self, participant: User) -> None:
        self.participants.append(participant)
        

    def remove_participant(self, participant: User) -> bool:
        for part in self.participants:
            if part == participant:
                self.participants.remove(participant)
        if self.participants == []:
            return True
        else:
            if participant == self.host:
                xpl = None
                for part in self.participants:
                    if xpl == None or part.xp > xpl.xp:
                        xpl = part
                self.host = xpl
            return False
    

    def sendmsg(self, msg: str, frm: User, server: ws.WebsocketServer) -> None:
        reply = [frm.name, msg, [frm.color[0], frm.color[1], frm.color[2]]]
        self.sendall(reply, server)
    

    def sysmsg(self, msg: str, server: ws.WebsocketServer) -> None:
        self.sendall(msg, server, 'sys')


    def sendall(self, msg: str | list, server: ws.WebsocketServer, header: str = 'msg') -> None:
        for cl in self.participants:
            cl.send(server, msg, header)


    def get_pos(self) -> dict:
        r = {}
        for cl in self.participants:
            r[cl] = [cl.x, cl.y]
        return r
    

    def move(self, server: ws.WebsocketServer) -> None:
        play = []
        for cli in self.participants:
            play.append([cli.name, [cli.x, cli.y], [cli.color[0], cli.color[1], cli.color[2]]])
        self.sendall(play, server, 'move')
