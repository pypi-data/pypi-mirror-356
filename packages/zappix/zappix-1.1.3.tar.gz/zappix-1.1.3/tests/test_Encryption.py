import unittest
import socket
import os
from zappix.get import Get
from tests import skip_integration_tests, skip_on_gitlab


zabbix_agent_address = 'localhost'


class TestPSK(unittest.TestCase):
    def setUp(self):
        self.get = Get(zabbix_agent_address)

    def test_key_length(self):
        self.get.set_psk_encryption('identity', 'af8ced32dfe8714e548694e2d29e1a14ba6fa13f216cb35c19d0feb1084b0429')
        self.assertEqual(32, len(self.get._psk))
        self.get.set_psk_encryption('identity', '0a' * 256)
        self.assertEqual(256, len(self.get._psk))

        with self.assertRaises(ValueError) as ve:
            self.get.set_psk_encryption('identity', '')
            self.assertEqual('PSK key lenght out of bounds', ve)
        with self.assertRaises(ValueError) as ve:
            self.get.set_psk_encryption('identity', 'a0' * 257)
            self.assertEqual('PSK key lenght out of bounds', ve)
            

    def test_identity_length(self):
        self.get.set_psk_encryption('identity', 'af8ced32dfe8714e548694e2d29e1a14ba6fa13f216cb35c19d0feb1084b0429')
        self.get.set_psk_encryption('i' * 128, 'af8ced32dfe8714e548694e2d29e1a14ba6fa13f216cb35c19d0feb1084b0429')
        self.assertEqual(128, len(self.get._psk_identity))
        with self.assertRaises(ValueError) as ve:
            self.get.set_psk_encryption('', 'af8ced32dfe8714e548694e2d29e1a14ba6fa13f216cb35c19d0feb1084b0429')
            self.assertEqual('PSK key lenght out of bounds', ve)
        with self.assertRaises(ValueError) as ve:
            self.get.set_psk_encryption('i' * 129, 'af8ced32dfe8714e548694e2d29e1a14ba6fa13f216cb35c19d0feb1084b0429')
            self.assertEqual('PSK key lenght out of bounds', ve)

    def test_key(self):
        with self.assertRaises(ValueError) as ve:
            self.get.set_psk_encryption('identity', 'nothex')
            self.assertEqual('he provided PSK key is not hexadecimal', ve)


@unittest.skipIf(skip_integration_tests, "Skipping integration tests")
@unittest.skipIf(skip_on_gitlab, "Skipping on GitLab")
class TestEncryptedConnection(unittest.TestCase):
    def setUp(self):
        self.get = Get(zabbix_agent_address)
        self.get.set_psk_encryption('identity', 'af8ced32dfe8714e548694e2d29e1a14ba6fa13f216cb35c19d0feb1084b0429')

    def test_get_value(self):
        resp = self.get.get_value("agent.ping")
        self.assertEqual(resp, '1')


if __name__ == '__main__':
    unittest.main()
