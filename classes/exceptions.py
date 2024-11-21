class UnrelatedException(Exception):
    errcodes = [0, 1, 2]
    errdic = ['user must be logged out to do this', 'user must be inside a room to do this', 'user can\'t be connected twice']

    def __init__(self, errcode: int = 0) -> None:
        """
        may be raised when a user tries something and nothing fails in the process but the user should not be abled to do it.

        <code>errcode: integer: </code> the error as an integer.<br>
        see UnrelatedException.errdic[errcode] for the string representation.
        """
        self.errcode = 0
        if errcode in self.errcodes:
            self.errcode = errcode
        self.errtxt = self.errdic[errcode]
        super().__init__('unhandled unrelated exception')
