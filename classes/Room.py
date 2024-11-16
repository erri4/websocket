from classes.User import User


class Room:
    blacklist: list[User] = []
    # banned people.


    def __init__(self, name: str, creator: User, password: str | None) -> None:
        """
        a class for managing client rooms.

        <code>name: string: </code> the name of the room.<br>
        <code>creator: User: </code> the creator of the room.<br>
        <code>password: string | None: </code> the password of the room.
        """
        self.name = name
        self.participants: list[User] = [creator]
        self.host: User = creator
        self.password = password


    def add_participant(self, participant: User) -> None:
        """
        add a participant.

        <code>participant: User: </code> the participant to be added.

        <code>return: None. </code>
        """
        self.participants.append(participant)
        

    def remove_participant(self, participant: User) -> bool:
        """
        remove a participant.

        <code>participant: User: </code> the participant to be removed.

        <code>return: boolean: </code> true if there are participants in the room and false if there isn't.
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
    

    def sendmsg(self, msg: str, frm: User) -> None:
        """
        send a message in the room.

        <code>msg: string: </code> the message to be sent.<br>
        <code>frm: User: </code> the user who sent the message.

        <code>return: None. </code>
        """
        reply = [frm.name, msg, [frm.color[0], frm.color[1], frm.color[2]]]
        self.sendall(reply)
    

    def sysmsg(self, msg: str) -> None:
        """
        send a system message (a message sent by the system).

        <code>msg: string: </code> the message to be sent.

        <code>return: None. </code>
        """
        self.sendall(msg, 'sys')


    def sendall(self, msg: str | list, header: str = 'msg') -> None:
        """
        send a message to all the participants in the room.

        <code>msg: string | list: </code> the message to be sent.<br>
        <code>header: string: </code> the header of the message.

        <code>return: None. </code>
        """
        for cl in self.participants:
            cl.send(msg, header)


    def move(self) -> None:
        """
        send the positions of the participants to every one of them.
        """
        play = []
        for cli in self.participants:
            play.append([cli.name, [cli.x, cli.y], [cli.color[0], cli.color[1], cli.color[2]]])
        self.sendall(play, 'move')
