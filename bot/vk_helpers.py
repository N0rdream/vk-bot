import requests
import json

def send_execute_request(code, access_token, api_version):
    url_execute = 'https://api.vk.com/method/execute'
    params = {
        'code': code,
        'v': api_version,
        'access_token': access_token
    }
    return requests.get(url_execute, params=params)

def construct_vkscript_message_sender(
        user_ids, access_token, api_version,
        message, vk_attachment_id
    ):
    params = {
        'user_ids': user_ids,
        'access_token': access_token,
        'api_version': api_version,   
    }
    if message is not None:
        params['message'] = message
    if vk_attachment_id is not None:
        params['attachment'] = vk_attachment_id
    return f'API.messages.send({json.dumps(params)})'

def construct_code_for_execute(data):
    return ';'.join(data) + ';'

