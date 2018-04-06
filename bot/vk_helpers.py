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
    if message:
        params['message'] = message
    if vk_attachment_id:
        params['attachment'] = vk_attachment_id
    return f'API.messages.send({json.dumps(params)})'

def combine_lines_into_code(lines):
    return ';'.join(lines) + ';'

def get_code_for_execute(data, access_token, api_version):
    lines = []
    for k in data:
        message, vk_attachment_id = k
        line = construct_vkscript_message_sender(
            list(data[k]), 
            access_token, 
            api_version, 
            message, 
            vk_attachment_id
        )
        lines.append(line)
    return combine_lines_into_code(lines)

