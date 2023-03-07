import unittest

from src.base64_decode import Base64Decode


class TestBase64Decode(unittest.TestCase):

    def test_base64_decode(self):
        params = {
            'task_id': 'task_1',
            'base64Value': 'SGVsbG8gV29ybGQ='
        }
        expected_output = 'Hello World'
        base64_decode = Base64Decode(params)
        base64_decode.execute()
        output_properties = base64_decode.get_output_properties()
        actual_output = output_properties['textValue']
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
