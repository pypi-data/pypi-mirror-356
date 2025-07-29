import unittest
from prime_sdk.base_response import BaseResponse

class TestBaseResponse(unittest.TestCase):
    def test_initialization(self):
        response_data = {
            'field1': 'value1',
            'field2': 123,
            'field3': {'nested_field': 'nested_value'},
            'field4': [{'list_field': 'list_value'}]
        }
        base_response = BaseResponse(response=response_data)

        self.assertEqual(base_response.response, response_data)
        self.assertEqual(base_response.response['field1'], 'value1')
        self.assertEqual(base_response.response['field2'], 123)
        self.assertEqual(base_response.response['field3']['nested_field'], 'nested_value')
        self.assertEqual(base_response.response['field4'][0]['list_field'], 'list_value')

    def test_str_representation(self):
        response_data = {'field1': 'value1'}
        base_response = BaseResponse(response=response_data)
        self.assertEqual(str(base_response), '{"field1": "value1"}')

if __name__ == '__main__':
    unittest.main() 