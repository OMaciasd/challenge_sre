from unittest.mock import patch
from app.app import app


@patch('app.app.initialize_rabbitmq')
def test_homepage(mock_initialize_rabbitmq):
    # Configura el mock para devolver valores predeterminados
    mock_initialize_rabbitmq.return_value = (None, None)

    # Crea un cliente de prueba para la aplicación Flask
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert response.data == b'Hello, World!'
