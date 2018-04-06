from django.test import TestCase
from .parsers import (
    get_hashtag_from_message, 
    process_incoming_data,
    parse_redis_data
)
from .vk_helpers import construct_vkscript_message_sender, get_code_for_execute


class GetHashtagFromMessageTestCase(TestCase):

    def test_getting_one_hashtag(self):
        actual_result = get_hashtag_from_message('rgg!#test()erfrf')
        self.assertEqual(actual_result, 'test')

    def test_getting_two_hashtags(self):
        actual_result = get_hashtag_from_message('#fIrSt#second')
        self.assertEqual(actual_result, 'first')

    def test_handling_empty_input(self):
        actual_result = get_hashtag_from_message('')
        self.assertIsNone(actual_result)


class ProcessIncomingDataTestCase(TestCase):

    def test_handling_confirmation_request(self):
        data = {
            'type': 'confirmation',
            'secret': 'secret',
            'group_id': 1
        }
        actual_result = process_incoming_data(data)
        correct_result = {
            'message_type': 'confirmation',
            'group_id': 1,
            'secret': 'secret'
        }
        self.assertEqual(actual_result, correct_result)

    def test_handling_regular_request(self):
        data = {
            'type': 'message',
            'secret': 'secret',
            'group_id': 1,
            'object': {
                'date': 1,
                'user_id': 1,
                'body': 'some_text'
            },
            'other': 'other_stuff'
        }
        actual_result = process_incoming_data(data)
        correct_result = {
            'message_type': 'message',
            'group_id': 1,
            'secret': 'secret',
            'vk_timestamp': 1,
            'message': 'some_text',
            'user_id': 1
        }
        self.assertEqual(actual_result, correct_result)

    def test_handling_incorrect_request(self):
        actual_result = process_incoming_data('incorrect')
        self.assertIsNone(actual_result)

    def test_handling_empty_request(self):
        actual_result = process_incoming_data('')
        self.assertIsNone(actual_result)


class ParseRedisDataTestCase(TestCase):

    def test_parsing_regular_data(self):
        data = {
            'task_1': '{"result": {"message": "text", "vk_attachment_id": 1, "user_id": 1}}',
            'task_2': '{"result": {"message": "text", "vk_attachment_id": 1, "user_id": 2}}',
        }
        actual_result = parse_redis_data(data)
        correct_result = {
            'data': {('text', 1): {1, 2}}, 
            'checked_keys': {'task_1', 'task_2'}
        }
        self.assertEqual(actual_result, correct_result)

    def test_parsing_with_user_ids_limit(self):
        data = {
            'task_1': '{"result": {"message": "text", "vk_attachment_id": 1, "user_id": 1}}',
            'task_2': '{"result": {"message": "text", "vk_attachment_id": 1, "user_id": 2}}',
            'task_3': '{"result": {"message": "text", "vk_attachment_id": 1, "user_id": 3}}',
        }
        actual_result = parse_redis_data(data, user_ids_limit=2)
        correct_results = [{
            'data': {('text', 1): {1, 2}}, 
            'checked_keys': {'task_1', 'task_2'}
        },
        {
            'data': {('text', 1): {2, 3}}, 
            'checked_keys': {'task_2', 'task_3'}
        },
        {
            'data': {('text', 1): {1, 3}}, 
            'checked_keys': {'task_1', 'task_3'}
        }]
        self.assertTrue(actual_result in correct_results)

    def test_parsing_with_execute_limit(self):
        data = {
            'task_1': '{"result": {"message": "one", "vk_attachment_id": 1, "user_id": 1}}',
            'task_2': '{"result": {"message": "two", "vk_attachment_id": 2, "user_id": 2}}',
            'task_3': '{"result": {"message": "three", "vk_attachment_id": 3, "user_id": 3}}',
        }
        actual_result = parse_redis_data(data, execute_limit=2)
        correct_results = [{
            'data': {('one', 1): {1}, ('two', 2): {2}}, 
            'checked_keys': {'task_1', 'task_2'}
        },
        {
            'data': {('two', 2): {2}, ('three', 3): {2}}, 
            'checked_keys': {'task_2', 'task_3'}
        },
        {
            'data': {('one', 1): {1}, ('three', 3): {3}}, 
            'checked_keys': {'task_1', 'task_3'}
        }]
        self.assertTrue(actual_result in correct_results)

    def test_parsing_incorrect_data(self):
        data = {
            'task_1': '"one"',
            'task_2': '"two"',
            'task_3': '"three"'
        }
        actual_result = parse_redis_data(data)
        correct_result = {
            'data': {}, 
            'checked_keys': {'task_1', 'task_2', 'task_3'}
        }
        self.assertEqual(actual_result, correct_result)


class ConstructVkscriptMessageSenderTestCase(TestCase):

    def test_construct_code(self):
        user_ids = [1, 2, 3]
        access_token = 'token'
        api_version = '5.73'
        message = 'text'
        vk_attachment_id = 'photo_123'
        actual_result = construct_vkscript_message_sender(
            user_ids, access_token, api_version,
            message, vk_attachment_id
        )
        correct_result = 'API.messages.send({' \
        '"user_ids": [1, 2, 3], ' \
        '"access_token": "token", ' \
        '"api_version": "5.73", ' \
        '"message": "text", ' \
        '"attachment": "photo_123"' \
        '})'
        self.assertEqual(actual_result, correct_result)


class GetCodeForExecuteTestCase(TestCase):

    def test_get_code_for_execute(self):
        data = {
            ('msg_1', 'attch_1'): {1, 2, 3}, 
            ('msg_2', 'attch_2'): {4, 5, 6, 7}
        }
        access_token = 'token'
        api_version = '5.73'
        actual_result = get_code_for_execute(data, access_token, api_version)
        code_1 = 'API.messages.send({' \
        '"user_ids": [1, 2, 3], ' \
        '"access_token": "token", ' \
        '"api_version": "5.73", ' \
        '"message": "msg_1", ' \
        '"attachment": "attch_1"' \
        '})'
        code_2 = 'API.messages.send({' \
        '"user_ids": [4, 5, 6, 7], ' \
        '"access_token": "token", ' \
        '"api_version": "5.73", ' \
        '"message": "msg_2", ' \
        '"attachment": "attch_2"' \
        '})'
        correct_result_1 = code_1 + ';' + code_2 + ';'
        correct_result_2 = code_2 + ';' + code_1 + ';'
        correct_results = [correct_result_1, correct_result_2]
        self.assertTrue(actual_result in correct_results)














































