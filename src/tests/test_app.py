import unittest
from unittest.mock import patch, MagicMock
from app import app, initialize_rabbitmq, initialize_database

class AppTestCase(unittest.TestCase):
    @patch('app.initialize_rabbitmq')
    @patch('app.initialize_database')
    def setUp(self, mock_initialize_database, mock_initialize_rabbitmq):

        self.mock_rabbitmq_connection = MagicMock()
        self.mock_rabbitmq_channel = MagicMock()
        mock_initialize_rabbitmq.return_value = (self.mock_rabbitmq_connection, self.mock_rabbitmq_channel)

        self.mock_database_engine = MagicMock()
        mock_initialize_database.return_value = self.mock_database_engine

        self.app = app.test_client()
        self.app.testing = True

    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.data, b"Hello, World!")
        self.assertEqual(response.status_code, 200)

    def test_log_data(self):
        response = self.app.post('/log', json={'message': 'test'})
        self.assertEqual(response.json, {'status': 'success', 'message': 'Log sent to RabbitMQ'})
        self.assertEqual(response.status_code, 200)
        self.mock_rabbitmq_channel.basic_publish.assert_called_once_with(
            exchange='',
            routing_key='data_queue',
            body='test'
        )

if __name__ == '__main__':
    unittest.main()
