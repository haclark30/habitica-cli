import unittest
from habitica import HabiticaAPI
import time

class TestHabitica(unittest.TestCase):
    def setUp(self):
        self.hbt_api = HabiticaAPI()

    def test_get_content(self):
        content = self.hbt_api.get_content()
        time_diff = time.time() - content['dateRetrieved']
        self.assertLess(time_diff, 86400)