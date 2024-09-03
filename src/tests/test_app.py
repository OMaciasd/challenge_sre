import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.config['TESTING'] = True

    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.data, b"Hello, World!")

    def test_log_data(self):
        response = self.app.post('/log', json={'message': 'Test log'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log sent to RabbitMQ', response.data)

if __name__ == '__main__':
    unittest.main()
