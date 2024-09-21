import platform
import socket
from app import create_app
from utils import log_utils
from utils.secrets_utils import validate_secrets


def get_host_ip(default='127.0.0.1'):
    current_os = platform.system()
    try:
        if current_os == "Linux":
            import netifaces
            interface = 'enp0s8'
            return netifaces.ifaddresses(
                interface
            )[
                netifaces.AF_INET
            ][
                0
            ][
                'addr'
            ]
        elif current_os == "Windows":
            return socket.gethostbyname(
                socket.gethostname(
                )
            )
        else:
            print(
                "Sistema operativo no soportado"
            )
            return default
    except (
        ValueError,
        KeyError,
        IndexError,
        ImportError
    ):
        return default


def main():
    validate_secrets()
    print("Starting the application...")

    log_message = 'Application started successfully'
    log_utils.send_log_to_rabbitmq(log_message)

    host_ip = get_host_ip()
    app = create_app()
    app.run(host=host_ip, port=5000, debug=True)


if __name__ == "__main__":
    main()
