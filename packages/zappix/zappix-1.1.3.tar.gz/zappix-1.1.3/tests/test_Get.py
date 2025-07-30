import unittest
from unittest.mock import patch, MagicMock
from zappix.get import Get
import socket
from tests import skip_integration_tests, skip_on_gitlab
from tests import zabbix_agent_address


class TestGet(unittest.TestCase):
    def setUp(self):
        self.msock = MagicMock()

    def test_init(self):
        get = Get('host')
        self.assertEqual(get._port, 10050)
        self.assertIsNone(get._source_address)

        get = Get('host', source_address='localhost')
        self.assertEqual(get._source_address, 'localhost')

    @patch('zappix.dstream.socket')
    def test_get_value(self, mock_socket):
        mock_socket.socket.return_value = self.msock
        self.msock.recv.side_effect = [
            b'ZBXD\x01\x01\x00\x00\x00\x00\x00\x00\x00', b'1', b''
            ]

        g = Get('localhost')
        result = g.get_value('agent.ping')

        self.assertEqual(result, '1')

    @patch('zappix.dstream.socket')
    def test_get_report(self, mock_socket):
        mock_socket.socket.return_value = self.msock
        self.msock.recv.side_effect = [
            b'ZBXD\x01\x01\x00\x00\x00\x00\x00\x00\x00', b'1',
            b'ZBXD\x01\x09\x00\x00\x00\x00\x00\x00\x00', b'localhost', b''
            ]

        g = Get('localhost')
        result = g.get_report(('agent.ping', 'system.hostname'))

        self.assertDictEqual(
            result,
            {'agent.ping': '1', 'system.hostname': 'localhost'}
        )


@unittest.skipIf(skip_on_gitlab, "Skipping on GitLab")
@unittest.skipIf(skip_integration_tests, "Skipping integration tests")
class TestGetValue(unittest.TestCase):
    def setUp(self):
        self.get = Get(zabbix_agent_address)

    def test_get_value(self):
        resp = self.get.get_value("agent.ping")
        self.assertEqual(resp, '1')

    def test_get_value_unsupported(self):
        resp = self.get.get_value("agent.pong")
        self.assertEqual(resp, 'ZBX_NOTSUPPORTED\x00Unsupported item key.')

    def test_get_report(self):
        resp = self.get.get_report(['agent.ping', 'agent.pong'])
        self.assertDictEqual(
            resp,
            {
                'agent.ping': '1',
                'agent.pong':
                'ZBX_NOTSUPPORTED\x00Unsupported item key.'
            }
        )


@unittest.skipIf(skip_on_gitlab, "Skipping on GitLab")
@unittest.skipIf(skip_integration_tests, "Skipping integration tests")
class TestGetValueWithBoundAddress(TestGetValue):
    def setUp(self):
        self.get = Get(zabbix_agent_address, source_address='localhost')


if __name__ == '__main__':
    unittest.main()
