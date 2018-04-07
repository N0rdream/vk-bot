from bot.vk_helpers import (
    construct_vkscript_message_sender,
    get_code_for_execute
)


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
