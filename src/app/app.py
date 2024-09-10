from . import create_app
from utils import log_utils
from utils.secrets_utils import validate_secrets


def main():
    validate_secrets()
    print("Starting the application...")

    log_message = 'Application started successfully'
    log_utils.send_log_to_rabbitmq(log_message)

    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":
    main()
