import unittest

from src.hello import Hello


class TestHello(unittest.TestCase):

    def test_hello(self):
        params = {
            'task_id': 'task_1',
            'yourName': 'World'
        }
        expected_output = 'Hello World'
        hello = Hello(params)
        hello.execute()
        output_properties = hello.get_output_properties()
        actual_output = output_properties['greeting']
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
