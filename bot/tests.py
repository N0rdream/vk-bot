from django.test import TestCase
from .parsers import (
    get_hashtag_from_message, 
    process_incoming_data,
    parse_redis_data
)
from .vk_helpers import (
    construct_vkscript_message_sender,
    get_code_for_execute
)


def test_getting_one_hashtag():
    assert get_hashtag_from_message('!!#test()') == 'test'

def test_getting_two_hashtags():
    assert get_hashtag_from_message('#fIrSt#second') == 'first'

def test_handling_empty_input():
    assert get_hashtag_from_message('') is None

def test_handling_confirmation_request():
    data = {
        'type': 'confirmation',
        'secret': 'secret',
        'group_id': 1
    }
    actual_result = process_incoming_data(data)
    expected_result = {
        'message_type': 'confirmation',
        'group_id': 1,
        'secret': 'secret'
    }
    assert actual_result == expected_result

def test_handling_regular_request():
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
    expected_result = {
        'message_type': 'message',
        'group_id': 1,
        'secret': 'secret',
        'vk_timestamp': 1,
        'message': 'some_text',
        'user_id': 1
    }
    assert actual_result == expected_result

def test_handling_incorrect_request():
    assert process_incoming_data('incorrect') is None

def test_handling_empty_request():
    assert process_incoming_data('') is None

def test_parsing_regular_data():
    data = {
        'task_1': '{"result": {"message": "text", "vk_attachment_id": 1, "user_id": 1}}',
        'task_2': '{"result": {"message": "text", "vk_attachment_id": 1, "user_id": 2}}',
    }
    actual_result = parse_redis_data(data)
    expected_result = {
        'data': {('text', 1): {1, 2}}, 
        'checked_keys': {'task_1', 'task_2'}
    }
    assert actual_result == expected_result

def test_parsing_with_user_ids_limit():
    data = {
        'task_1': '{"result": {"message": "text", "vk_attachment_id": 1, "user_id": 1}}',
        'task_2': '{"result": {"message": "text", "vk_attachment_id": 1, "user_id": 2}}',
        'task_3': '{"result": {"message": "text", "vk_attachment_id": 1, "user_id": 3}}',
    }
    actual_result = parse_redis_data(data, user_ids_limit=2)
    expected_results = [{
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
    assert actual_result in expected_results

def test_parsing_with_execute_limit():
    data = {
        'task_1': '{"result": {"message": "one", "vk_attachment_id": 1, "user_id": 1}}',
        'task_2': '{"result": {"message": "two", "vk_attachment_id": 2, "user_id": 2}}',
        'task_3': '{"result": {"message": "three", "vk_attachment_id": 3, "user_id": 3}}',
    }
    actual_result = parse_redis_data(data, execute_limit=2)
    expected_results = [{
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
    assert actual_result in expected_results

def test_parsing_incorrect_data():
    data = {
        'task_1': '"one"',
        'task_2': '"two"',
        'task_3': '"three"'
    }
    actual_result = parse_redis_data(data)
    expected_result = {
        'data': {}, 
        'checked_keys': {'task_1', 'task_2', 'task_3'}
    }
    assert actual_result == expected_result


def test_construct_code():
    user_ids = [1, 2, 3]
    access_token = 'token'
    api_version = '5.73'
    message = 'text'
    vk_attachment_id = 'photo_123'
    actual_result = construct_vkscript_message_sender(
        user_ids, access_token, api_version,
        message, vk_attachment_id
    )
    expected_result = 'API.messages.send({' \
    '"user_ids": [1, 2, 3], ' \
    '"access_token": "token", ' \
    '"api_version": "5.73", ' \
    '"message": "text", ' \
    '"attachment": "photo_123"' \
    '})'
    assert actual_result == expected_result

def test_get_code_for_execute():
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
    expected_result_1 = code_1 + ';' + code_2 + ';'
    expected_result_2 = code_2 + ';' + code_1 + ';'
    expected_results = [expected_result_1, expected_result_2]
    assert actual_result in expected_results














































