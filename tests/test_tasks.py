import unittest

from app.example_abort import ExampleAbort
from app.example_api import ExampleApi


class TestTasks(unittest.TestCase):
    """
    A unit test class for testing the functionality of the ExampleApi and ExampleAbort tasks.
    """

    def test_example_api(self):
        """
        Test the ExampleApi task.
        """
        params = {'task_id': 'task_1', 'productId': '1'}
        expected_output = {'productName': 'iPhone 9', 'brand': 'Apple'}
        example_api = ExampleApi(params)
        self.execute_test(example_api, expected_output)

    def test_example_abort(self):
        """
        Test the ExampleAbort task.
        """
        server = {'url': 'https://httpbin.org', 'username': 'user', 'password': 'login',
                  'authenticationMethod': 'Basic'}
        params = {'task_id': 'task_2', 'server': server, 'retryWaitingTime': 5, 'retryCount': 5, 'username': '',
                  'password': ''}
        expected_output = {'statusCode': 200}
        example_abort = ExampleAbort(params)
        self.execute_test(example_abort, expected_output)

    def execute_test(self, task_obj, expected_output):
        """
        Execute a task and assert that its output matches the expected output.

        Parameters:
            task_obj (BaseTask): The task object to execute.
            expected_output (dict): The expected output of the task.
        """
        task_obj.execute()
        actual_output = task_obj.get_output_properties()
        self.assertEqual(expected_output, actual_output)


if __name__ == '__main__':
    unittest.main()
