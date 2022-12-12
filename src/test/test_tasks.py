import unittest

from src.main.python.example_abort import ExampleAbort
from src.main.python.example_api import ExampleApi


# Test command: python -m unittest src\test\test_tasks.py

class TestTasks(unittest.TestCase):

    def test_example_api(self):
        params = {'task_id': 'task_1', 'productId': '1'}
        expected_output = {'productName': 'iPhone 9', 'brand': 'Apple'}
        example_api = ExampleApi(params)
        self.execute('Example API', example_api, expected_output)

    def test_example_abort(self):
        server = {'url': 'https://httpbin.org', 'username': 'user', 'password': 'login',
                  'authenticationMethod': 'Basic'}
        params = {'task_id': 'task_2', 'server': server, 'retryWaitingTime': 5, 'retryCount': 5, 'username': '',
                  'password': ''}
        expected_output = {'statusCode': 200}
        example_abort = ExampleAbort(params)
        self.execute('Example Abort', example_abort, expected_output)

    def execute(self, test_name, task_obj, expected_output):
        task_obj.execute()
        actual_output = task_obj.get_output_properties()
        print(f"{test_name} expected output : {expected_output}")
        print(f"{test_name} actual output : {actual_output}\n")
        self.assertEqual(expected_output, actual_output)


if __name__ == '__main__':
    unittest.main()
