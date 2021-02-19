# Imports.
import unittest
import shutil

# Import resources.
from server import app


class BaseCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        shutil.rmtree("./static", ignore_errors=True)
