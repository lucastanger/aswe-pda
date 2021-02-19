import unittest

from app import app


class TestEventsToday(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_events_today(self):
        response = self.app.get('/rest/api/v1/events/today')

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
