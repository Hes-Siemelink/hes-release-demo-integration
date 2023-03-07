import unittest

from src.dummy_json import DummyJson


class TestDummyJson(unittest.TestCase):

    def test_dummy_json(self):
        server = {
            'url': 'https://dummyjson.com',
            'username': 'admin',
            'password': 'admin',
            'authenticationMethod': 'Basic'
        }
        params = {
            'task_id': 'task_1',
            'productId': '1',
            'server': server
        }
        expected_output = 'iPhone 9'
        dummy_json = DummyJson(params)
        dummy_json.execute()
        output_properties = dummy_json.get_output_properties()
        actual_output = output_properties['productName']
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
