import unittest
from zappix.protocol import ServerRequest, ModelEncoder
import json
from ast import literal_eval


class TestServerRequest(unittest.TestCase):
    def test_queue_overview(self):
        req = ServerRequest('queue.get', 'overview', 'nosid')
        tested = json.dumps(req, cls=ModelEncoder)
        expected = {"request": "queue.get", "type": "overview", "sid": "nosid"}
        self.assertEqual(literal_eval(tested), expected)

    def test_queue_overview_by_proxy(self):
        req = ServerRequest('queue.get', 'overview by proxy', 'nosid')
        tested = json.dumps(req, cls=ModelEncoder)
        expected = {"request": "queue.get", "type": "overview by proxy", "sid": "nosid"}
        self.assertEqual(literal_eval(tested), expected)

    def test_queue_details(self):
        req = ServerRequest('queue.get', 'details', 'nosid', limit=100)
        tested = json.dumps(req, cls=ModelEncoder)
        expected = {"request": "queue.get", "type": "details", "limit": "100", "sid": "nosid"}
        self.assertEqual(literal_eval(tested), expected)

    def test_item_test(self):
        payload = {"options":{"single":False,"state":0},"item":{"value":"1","value_type":"3"}}
        req = ServerRequest('item.test', 'item.test', 'nosid', item_data=payload)
        tested = json.dumps(req, cls=ModelEncoder)
        expected =  {"request":"item.test","data":{"options":{"single":False,"state":0},"item":{"value":"1","value_type":"3"}},"sid":"nosid"}
        self.assertDictEqual(json.loads(tested), expected)

    def test_item_preprocessing(self):
        payload = {
                    "value": "",
                    "steps": [
                        {
                            "type": "21",
                            "error_handler": "0",
                            "error_handler_params": "",
                            "params": "Zabbix.sleep(10000);\nreturn value;"
                        }
                    ],
                    "single": True,
                    "state": 0,
                    "value_type": "3"
                }
        req = ServerRequest('preprocessing.test', 'item.test', 'nosid', item_data=payload)
        tested = json.dumps(req, cls=ModelEncoder)
        expected =  {"request":"preprocessing.test","data":{                    "value": "",
                    "steps": [
                        {
                            "type": "21",
                            "error_handler": "0",
                            "error_handler_params": "",
                            "params": "Zabbix.sleep(10000);\nreturn value;"
                        }
                    ],
                    "single": True,
                    "state": 0,
                    "value_type": "3"},"sid":"nosid"}
        self.assertDictEqual(json.loads(tested), expected)
