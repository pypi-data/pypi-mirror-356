import unittest
from zappix.dstream import _Dstream


class TestDstream(unittest.TestCase):
    def test_response_after_sending_collected_data(self):
        response = _Dstream._parse_server_response(
            '{"response":"success", "info":"processed: 3; failed: 0; total: 3; seconds spent: 0.003534"}'
        )
        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 3)
        self.assertEqual(response.failed, 0)
        self.assertEqual(response.total, 3)
        self.assertAlmostEqual(response.seconds_spent, 0.003534)
