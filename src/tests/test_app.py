import unittest
from unittest.mock import patch
from app.app import app

class FlaskAppTests(unittest.TestCase):
    
    @patch('app.app.initialize_rabbitmq')
    def test_homepage(self, mock_initialize_rabbitmq):
        mock_initialize_rabbitmq.return_value = (None, None)

        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'Hello, World!')

if __name__ == '__main__':
    unittest.main()
