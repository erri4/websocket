from app import app
from ws import start_server
from func import get_ip


def main() -> None:
    start_server(get_ip())


if __name__ == 'main':
    main()
