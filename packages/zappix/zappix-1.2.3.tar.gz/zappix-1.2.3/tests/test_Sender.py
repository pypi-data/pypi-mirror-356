from pyzabbix import ZabbixAPI
from unittest.mock import patch, MagicMock
from zappix.protocol import SenderDataRequest, SenderData
from zappix.sender import Sender
import os
import random
import socket
import tempfile
import time
import unittest
from tests.utils import create_host, create_item, remove_host
from tests import skip_integration_tests, skip_on_gitlab
from tests import zabbix_server_address
from tests import zabbix_api_address, zabbix_default_user, zabbix_default_password


class TestSender(unittest.TestCase):
    def setUp(self):
        self.msock = MagicMock()

    def test_init(self):
        get = Sender('host')
        self.assertEqual(get._port, 10051)
        self.assertIsNone(get._source_address)

        get = Sender('host', source_address='localhost')
        self.assertEqual(get._source_address, 'localhost')

    @patch('zappix.dstream.socket')
    def test_get_value(self, mock_socket):
        mock_socket.socket.return_value = self.msock
        self.msock.recv.side_effect = [
            b'ZBXD\x01\x5b\x00\x00\x00\x00\x00\x00\x00',
            b'{"response":"success", "info":"processed: 1; failed: 0; total: 1; seconds spent: 0.060753"}', b''
            ]

        s = Sender('localhost')
        response = s.send_value('testhost', 'test', 1)

        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 1)
        self.assertEqual(response.failed, 0)
        self.assertEqual(response.total, 1)
        self.assertAlmostEqual(response.seconds_spent, 0.060753)


    @patch('zappix.dstream.socket')
    def test_send_file(self, mock_socket):
        file_ = tempfile.NamedTemporaryFile('w+', delete=False)
        file_.write("testhost test 1\n"
                    "testhost test  2\n"
                    "testhost test   3\n")
        file_.close()
        mock_socket.socket.return_value = self.msock
        self.msock.recv.side_effect = [
            b'ZBXD\x01\x5b\x00\x00\x00\x00\x00\x00\x00',
            b'{"response":"success", "info":"processed: 3; failed: 0; total: 3; seconds spent: 0.060753"}', b''
            ]

        sender = Sender('localhost')
        response, _ = sender.send_file(file_.name)
        os.unlink(file_.name)
        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 3)
        self.assertEqual(response.failed, 0)
        self.assertEqual(response.total, 3)
        self.assertAlmostEqual(response.seconds_spent, 0.060753)

    @patch('zappix.dstream.socket')
    def test_send_decorator(self, mock_socket):
        mock_socket.socket.return_value = self.msock
        self.msock.recv.side_effect = [
            b'ZBXD\x01\x5b\x00\x00\x00\x00\x00\x00\x00',
            b'{"response":"success", "info":"processed: 1; failed: 0; total: 1; seconds spent: 0.060753"}', b''
            ]

        sender = Sender('host')

        @sender.send_result('testhost', 'test')
        def echo(number):
            return number

        number = random.randint(1, 100)
        res = echo(number)
        self.assertEqual(res, number)

    @patch('zappix.dstream.socket')
    def test_send_bulk(self, mock_socket):
        mock_socket.socket.return_value = self.msock
        self.msock.recv.side_effect = [
            b'ZBXD\x01\x5b\x00\x00\x00\x00\x00\x00\x00',
            b'{"response":"success", "info":"processed: 2; failed: 0; total: 2; seconds spent: 0.060753"}', b''
            ]

        rq = [
                SenderData('localhost', 'test.key', 1),
                SenderData('Zabbix server', 'test.key2', "test_value"),
            ]
        

        sender = Sender('host')
        response = sender.send_bulk(rq)
        self.msock.sendall.assert_called_with(b'ZBXD\x01\xa0\x00\x00\x00\x00\x00\x00\x00{"request": "sender data", "data": [{"host": "localhost", "key": "test.key", "value": 1}, {"host": "Zabbix server", "key": "test.key2", "value": "test_value"}]}')
        
        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 2)
        self.assertEqual(response.failed, 0)
        self.assertEqual(response.total, 2)
        self.assertAlmostEqual(response.seconds_spent, 0.060753)


class TestFileParser(unittest.TestCase):
    def test_file_without_timestamps(self):
        file_ = tempfile.NamedTemporaryFile('w+', delete=False)
        file_.write("testhost test 1\n"
                    "testhost test  2\n"
                    "testhost test   3")
        file_.close()

        payload, failed = Sender.parse_data_file(file_.name)
        self.assertListEqual(failed, [])
        self.assertEqual(len(payload), 3)
        for i in range(3):
            with self.subTest(i=i):
                self.assertSequenceEqual([payload[i].host, payload[i].key, payload[i].value], ['testhost', 'test', str(i+1)])

        os.unlink(file_.name)

    def test_file_with_timestamps(self):
        file_ = tempfile.NamedTemporaryFile('w+', delete=False)
        file_.write("testhost test 1618608771 1\n"
                    "testhost test 1618608772 2\n"
                    "testhost test  1618608773 3\n")
        file_.close()

        payload, failed = Sender.parse_data_file(file_.name, with_timestamps=True)
        self.assertListEqual(failed, [])
        self.assertEqual(len(payload), 3)
        for i in range(3):
            with self.subTest(i=i):
                self.assertSequenceEqual([payload[i].host, payload[i].key, payload[i].clock, payload[i].value], ['testhost', 'test', 1618608771 + i, str(i+1)])

        os.unlink(file_.name)

    def test_file_with_timestamps_ns(self):
        file_ = tempfile.NamedTemporaryFile('w+', delete=False)
        file_.write("testhost test 1618608771 100000001 1\n"
                    "testhost test 1618608771  100000002 2\n"
                    "testhost test  1618608771 100000003 3\n")
        file_.close()

        payload, failed = Sender.parse_data_file(file_.name, with_timestamps=True, with_ns=True)
        self.assertListEqual(failed, [])
        self.assertEqual(len(payload), 3)
        for i in range(3):
            with self.subTest(i=i):
                self.assertSequenceEqual([payload[i].host, payload[i].key, payload[i].clock, payload[i].ns, payload[i].value], ['testhost', 'test', 1618608771, 100000001 + i, str(i+1)])

        os.unlink(file_.name)

    def test_file_without_timestamps_missing_value(self):
        file_ = tempfile.NamedTemporaryFile('w+', delete=False)
        file_.write("testhost test 1\n"
                    "testhost test \n"
                    "testhost test 3\n")
        file_.close()

        payload, failed = Sender.parse_data_file(file_.name)
        self.assertListEqual(failed, [2])
        self.assertEqual(len(payload), 2)
        self.assertSequenceEqual([payload[0].host, payload[0].key, payload[0].value], ['testhost', 'test', '1'])
        self.assertSequenceEqual([payload[1].host, payload[1].key, payload[1].value], ['testhost', 'test', '3'])

    def test_file_with_timestamps_missing_value(self):
        file_ = tempfile.NamedTemporaryFile('w+', delete=False)
        file_.write("testhost test 1618608771 1\n"
                    "testhost test 1618608772\n"
                    "testhost test     3\n")
        file_.close()

        payload, failed = Sender.parse_data_file(file_.name, with_timestamps=True)
        self.assertListEqual(failed, [2, 3])
        self.assertEqual(len(payload), 1)
        self.assertSequenceEqual([payload[0].host, payload[0].key, payload[0].clock, payload[0].value], ['testhost', 'test', 1618608771, '1'])

    def test_file_with_timestamps_ns_missing_value(self):
        file_ = tempfile.NamedTemporaryFile('w+', delete=False)
        file_.write("testhost test 1618608771 100000001 1\n"
                    "testhost test 1618608772 100000001\n"
                    "testhost test     3\n")
        file_.close()

        payload, failed = Sender.parse_data_file(file_.name, with_timestamps=True, with_ns=True)
        self.assertListEqual(failed, [2, 3])
        self.assertEqual(len(payload), 1)
        self.assertSequenceEqual([payload[0].host, payload[0].key, payload[0].clock, payload[0].ns, payload[0].value], ['testhost', 'test', 1618608771, 100000001, '1'])


class _BaseIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sender = Sender(zabbix_server_address)
        cls.zapi = ZabbixAPI(zabbix_api_address)
        cls.zapi.login(zabbix_default_user, zabbix_default_password)
        cls.hostid = create_host(cls.zapi, 'testhost')
        create_item(cls.zapi, cls.hostid)

        CacheUpdateFrequency = 5
        time.sleep(CacheUpdateFrequency)

    @classmethod
    def tearDownClass(cls):
        remove_host(cls.zapi, cls.hostid)
        cls.zapi.user.logout()


@unittest.skipIf(skip_integration_tests, "Skipping integration tests")
class TestSenderValue(_BaseIntegrationTest):
    def test_send_single_value(self):
        response = self.sender.send_value('testhost', 'test', 1)
        
        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 1)
        self.assertEqual(response.failed, 0)
        self.assertEqual(response.total, 1)
        

    @unittest.skip("Behaviour inconsistent across Zabbix versions")
    def test_send_bad_value(self):
        response = self.sender.send_value('testhost', 'test', "bad_value")

        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 0)
        self.assertEqual(response.failed, 1)
        self.assertEqual(response.total, 1)


    def test_send_bad_key(self):
        response = self.sender.send_value('testhost', 'bad_key', 1)
        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 0)
        self.assertEqual(response.failed, 1)
        self.assertEqual(response.total, 1)


    def test_send_bad_hostname(self):
        response = self.sender.send_value('bad_host', 'test', 1)
        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 0)
        self.assertEqual(response.failed, 1)
        self.assertEqual(response.total, 1)

    def test_send_bad_server(self):
        sender = Sender('nonexisting-server')
        with self.assertRaises(socket.gaierror):
            resp = sender.send_value('testhost', 'test', 1)

    def test_send_bad_port(self):
        sender = Sender(zabbix_server_address, 666)
        with self.assertRaises(ConnectionRefusedError):
            resp = sender.send_value('testhost', 'test', 1)


@unittest.skipIf(skip_integration_tests, "Skipping integration tests")
class TestSenderFile(_BaseIntegrationTest):
    def test_send_file(self):
        file_ = tempfile.NamedTemporaryFile('w+', delete=False)
        file_.write("testhost test 1\n"
                    "testhost test  2\n"
                    "testhost test   3\n")
        file_.close()
        response, _ = self.sender.send_file(file_.name)
        os.unlink(file_.name)
        
        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 3)
        self.assertEqual(response.failed, 0)
        self.assertEqual(response.total, 3)


    def test_send_corrupted_file(self):
        file_ = tempfile.NamedTemporaryFile('w+', delete=False)
        file_.write("testhost test 1\n"
                    "testhost test\n"
                    "testhost test \n"
                    "testhost test 3\n")
        file_.close()
        response, corrupted_lines = self.sender.send_file(file_.name)
        os.unlink(file_.name)
        self.assertSequenceEqual(corrupted_lines, [2, 3])
        
        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 2)
        self.assertEqual(response.failed, 0)
        self.assertEqual(response.total, 2)


    def test_send_file_with_timestamps(self):
        file_ = tempfile.NamedTemporaryFile('w+', delete=False)
        file_.write("testhost test {t} 10\n"
                    "testhost test  {t}  20\n"
                    "testhost   test {t} 30\n".format(t=int(time.time()//1)))
        file_.close()
        response, _ = self.sender.send_file(file_.name, with_timestamps=True)
        os.unlink(file_.name)
        
        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 3)
        self.assertEqual(response.failed, 0)
        self.assertEqual(response.total, 3)


    def test_send_file_with_timestamps_ns(self):
        file_ = tempfile.NamedTemporaryFile('w+', delete=False)
        file_.write("testhost test {t} 100000001 10\n"
                    "testhost test  {t} 100000002 20\n"
                    "testhost   test {t} 100000003 30\n".format(t=int(time.time()//1)))
        file_.close()
        response, _ = self.sender.send_file(file_.name, with_timestamps=True, with_ns=True)
        os.unlink(file_.name)
 
        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 3)
        self.assertEqual(response.failed, 0)
        self.assertEqual(response.total, 3)


    def test_send_corrupted_file_with_timestamps(self):
        file_ = tempfile.NamedTemporaryFile('w+', delete=False)
        file_.write("testhost test {t} 10\n"
                    "testhost test\n"
                    "testhost   test {t} \n"
                    "testhost test {t} 2\n".format(t=int(time.time()//1)))
        file_.close()
        response, corrupted_lines = self.sender.send_file(
            file_.name,
            with_timestamps=True
        )
        os.unlink(file_.name)
        self.assertSequenceEqual(corrupted_lines, [2, 3])
        
        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 2)
        self.assertEqual(response.failed, 0)
        self.assertEqual(response.total, 2)


    def test_send_corrupted_file_with_timestamps_ns(self):
        file_ = tempfile.NamedTemporaryFile('w+', delete=False)
        file_.write("testhost test {t} 100000001 10\n"
                    "testhost test\n"
                    "testhost   test {t} 100000002\n"
                    "testhost test {t} 100000003 2\n".format(t=int(time.time()//1)))
        file_.close()
        response, corrupted_lines = self.sender.send_file(
            file_.name,
            with_timestamps=True,
            with_ns=True
        )
        os.unlink(file_.name)
        self.assertSequenceEqual(corrupted_lines, [2, 3])
        
        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 2)
        self.assertEqual(response.failed, 0)
        self.assertEqual(response.total, 2)


@unittest.skipIf(skip_integration_tests, "Skipping integration tests")
class TestSenderBulk(_BaseIntegrationTest):
    def test_send_bulk(self):
        rq = [
                SenderData('testhost', 'test', 1),
                SenderData('testhost', 'test', 20),
            ]

        rq.append(SenderData('testhost', 'test', 300))

        response = self.sender.send_bulk(rq)
        
        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 3)
        self.assertEqual(response.failed, 0)
        self.assertEqual(response.total, 3)
 

    def test_send_bulk_with_timestamp(self):
        now = int(time.time()//1)
        rq = [
                SenderData('testhost', 'test', 1, now),
                SenderData('testhost', 'test', 20, now + 1),
            ]
        

        rq.append(SenderData('testhost', 'test', 300, now + 2))

        response = self.sender.send_bulk(rq, with_timestamps=True)

        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 3)
        self.assertEqual(response.failed, 0)
        self.assertEqual(response.total, 3)


@unittest.skipIf(skip_on_gitlab, "Skipping on GitLab")
@unittest.skipIf(skip_integration_tests, "Skipping integration tests")
class TestSenderValueWithBoundAddress(TestSenderValue):
    def setUp(self):
        self.sender = Sender(zabbix_server_address, source_address='localhost')


@unittest.skipIf(skip_integration_tests, "Skipping integration tests")
class TestSenderDecorator(_BaseIntegrationTest):
    def test_send_single_value(self):
        @self.sender.send_result('testhost', 'test')
        def echo(number):
            return number

        number = random.randint(1, 100)
        res = echo(number)
        self.assertEqual(res, number)

@unittest.skipIf(skip_integration_tests, "Skipping integration tests")
class TestSenderCompressedValue(_BaseIntegrationTest):
    def test_send_single_value(self):
        self.sender.compress = True
        response = self.sender.send_value('testhost', 'test', 1)
        
        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 1)
        self.assertEqual(response.failed, 0)
        self.assertEqual(response.total, 1)
        

if __name__ == '__main__':
    unittest.main()
