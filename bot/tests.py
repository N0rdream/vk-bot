from django.test import TestCase
from .parsers import (
    get_hashtag_from_message, 
    process_incoming_data,
    parse_redis_data
)
from .vk_helpers import construct_vkscript_message_sender


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
            'task_1': '{"result": {"hashtag": "test", "user_id": 1}}',
            'task_2': '{"result": {"hashtag": "test", "user_id": 2}}'
        }
        actual_result = parse_redis_data(data)
        correct_result = {
            'data': {'test': {1, 2}}, 
            'checked_keys': {'task_1', 'task_2'}
        }
        self.assertEqual(actual_result, correct_result)

    def test_parsing_with_user_ids_limit(self):
        data = {
            'task_1': '{"result": {"hashtag": "test", "user_id": 1}}',
            'task_2': '{"result": {"hashtag": "test", "user_id": 2}}',
            'task_3': '{"result": {"hashtag": "test", "user_id": 3}}'
        }
        actual_result = parse_redis_data(data, user_ids_limit=2)
        correct_results = [{
            'data': {'test': {1, 2}}, 
            'checked_keys': {'task_1', 'task_2'}
        },
        {
            'data': {'test': {2, 3}}, 
            'checked_keys': {'task_2', 'task_3'}
        },
        {
            'data': {'test': {1, 3}}, 
            'checked_keys': {'task_1', 'task_3'}
        }]
        self.assertTrue(actual_result in correct_results)

    def test_parsing_with_execute_limit(self):
        data = {
            'task_1': '{"result": {"hashtag": "one", "user_id": 1}}',
            'task_2': '{"result": {"hashtag": "two", "user_id": 2}}',
            'task_3': '{"result": {"hashtag": "three", "user_id": 3}}'
        }
        actual_result = parse_redis_data(data, execute_limit=2)
        correct_results = [{
            'data': {'one': {1}, 'two': {2}}, 
            'checked_keys': {'task_1', 'task_2'}
        },
        {
            'data': {'two': {2}, 'three': {2}}, 
            'checked_keys': {'task_2', 'task_3'}
        },
        {
            'data': {'one': {1}, 'three': {3}}, 
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




















































