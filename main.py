from app import app
from ws import start_server
from func import get_ip


def main() -> None:
    """
    start the websocket server. the flask server is started automaticly with the flask run command.
    """
    start_server(get_ip())


if __name__ == 'main':
    main()
