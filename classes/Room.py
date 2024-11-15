from classes.User import User
import websocket_server as ws


class Room:
    """
    a class for managing client rooms.
    """
    blacklist: list[User] = []
    # banned people.


    def __init__(self, name: str, creator: User, password: str | None) -> None:
        """
        set the name, host, password and the first participant.
        """
        self.name = name
        self.participants: list[User] = [creator]
        self.host: User = creator
        self.password = password


    def add_participant(self, participant: User) -> None:
        """
        add a participant.

        <code>participant: User:</code> the participant to be added.

        <code>return: None.</code>
        """
        self.participants.append(participant)
        

    def remove_participant(self, participant: User) -> bool:
        """
        remove a participant.

        <code>participant: User:</code> the participant to be removed.

        <code>return: boolean:</code> true if there are participants in the room and false if there isn't.
        """
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
        """
        send a message in the room.

        <code>msg: string:</code> the message to be sent.<br>
        <code>frm: User:</code> the user who sent the message.<br>
        <code>server: WebsocketServer:</code> the server to send the message with.

        <code>return: None.</code>
        """
        reply = [frm.name, msg, [frm.color[0], frm.color[1], frm.color[2]]]
        self.sendall(reply, server)
    

    def sysmsg(self, msg: str, server: ws.WebsocketServer) -> None:
        """
        send a system message (a message sent by the system).

        <code>msg: string:</code> the message to be sent.<br>
        <code>sever: WebsocketServer:</code> the server to send the message with.

        <code>return: None.</code>
        """
        self.sendall(msg, server, 'sys')


    def sendall(self, msg: str | list, server: ws.WebsocketServer, header: str = 'msg') -> None:
        """
        send a message to all the participants in the room.

        <code>msg: string | list:</code> the message to be sent.<br>
        <code>sever: WebsocketServer:</code> the server to send the message with.<br>
        <code>header: string:</code> the header of the message.

        <code>return: None.</code>
        """
        for cl in self.participants:
            cl.send(server, msg, header)


    def move(self, server: ws.WebsocketServer) -> None:
        """
        send the positions of the participants to every one of them.

        <code>server: WebsocketServer:</code> the server to send the positions with.

        <code>return: None.</code>
        """
        play = []
        for cli in self.participants:
            play.append([cli.name, [cli.x, cli.y], [cli.color[0], cli.color[1], cli.color[2]]])
        self.sendall(play, server, 'move')
