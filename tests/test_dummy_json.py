import unittest

from src.dummy_json import DummyJson


class TestDummyJson(unittest.TestCase):
    server = {
        'url': 'https://dummyjson.com',
        'username': 'admin',
        'password': 'admin',
        'authenticationMethod': 'Basic'
    }

    def test_valid_product_id(self):
        params = {
            'task_id': 'task_1',
            'productId': '1',
            'server': self.server
        }
        expected_output = 'iPhone 9'
        dummy_json = DummyJson(params)
        dummy_json.execute()
        output_properties = dummy_json.get_output_properties()
        actual_output = output_properties['productName']
        self.assertEqual(actual_output, expected_output)

    def test_invalid_product_id(self):
        params = {
            'task_id': 'task_1',
            'productId': '500',
            'server': self.server
        }
        expected_output = None
        dummy_json = DummyJson(params)
        dummy_json.execute()
        output_properties = dummy_json.get_output_properties()
        actual_output = output_properties['productName']
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
