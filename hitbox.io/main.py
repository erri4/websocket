from app import app
from ws import start_server


def main() -> None:
    """
    start the websocket server. the flask server is started automaticly with the flask run command.
    """
    start_server()


if __name__ == 'main':
    main()
