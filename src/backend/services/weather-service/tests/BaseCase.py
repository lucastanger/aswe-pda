# Imports.
import unittest

# Import resources.
from server import app


class BaseCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass
