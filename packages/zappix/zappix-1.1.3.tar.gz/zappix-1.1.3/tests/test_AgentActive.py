import unittest
import time
from zappix.agent_active import AgentActive
from zappix.protocol import AgentDataRequest, AgentData, ServerInfo
from pyzabbix import ZabbixAPI
from tests.utils import create_host, create_item, remove_host
from tests import skip_integration_tests, zabbix_server_address
from tests import zabbix_api_address, zabbix_default_user, zabbix_default_password


class _BaseIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.active = AgentActive('testhost', zabbix_server_address)
        cls.zapi = ZabbixAPI(zabbix_api_address)
        cls.zapi.login(zabbix_default_user, zabbix_default_password)
        cls.hostid = create_host(cls.zapi, 'testhost')
        create_item(cls.zapi, cls.hostid, 7)

        CacheUpdateFrequency = 5
        time.sleep(CacheUpdateFrequency)

    @classmethod
    def tearDownClass(cls):
        remove_host(cls.zapi, cls.hostid)
        cls.zapi.user.logout()


class TestAgentActiveParser(unittest.TestCase):
    def test_active_check_parser(self):
        response_active_items = (
            '{"response":"success",'
            '"data":['
            '{"key":"log[/home/zabbix/logs/zabbix_agentd.log]",'
            '"delay":30,'
            '"lastlogsize":0,'
            '"mtime":0},'
            '{"key":"agent.version",'
            '"delay":600,'
            '"lastlogsize":0,'
            '"mtime":0}]}')
        response = AgentActive._parse_active_check_list(response_active_items)
        self.assertEqual(len(response), 2)

        # Note: order of items is reversed due to while/pop
        self.assertEqual(response[0].key,
                         "log[/home/zabbix/logs/zabbix_agentd.log]")
        self.assertEqual(response[0].delay, 30)
        self.assertEqual(response[0].lastlogsize, 0)
        self.assertEqual(response[0].mtime, 0)


@unittest.skipIf(skip_integration_tests, "Skipping integration tests")
class TestAgentActive(_BaseIntegrationTest):
    def test_get_active_checks(self):
        checks = self.active.get_active_checks()
        self.assertIsNotNone(checks)
        self.assertEqual(len(checks), 1)

        self.assertEqual(checks[0].key, 'test')

    def test_send_agent_active_values(self):
        item_value = AgentData('testhost', 'test', 20, int(time.time()//1), 0)
        data = AgentDataRequest([item_value])
        response = self.active.send_collected_data(data)

        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 1)
        self.assertEqual(response.failed, 0)
        self.assertEqual(response.total, 1)


if __name__ == '__main__':
    unittest.main()
