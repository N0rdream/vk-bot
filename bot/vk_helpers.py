import requests


def send_execute_request(code, access_token, api_version):
    url_execute = 'https://api.vk.com/method/execute'
    params = {
        'code': code,
        'v': api_version,
        'access_token': access_token
    }
    return requests.get(url_execute, params=params)

def construct_vkscript_message_sender(user_ids, access_token, api_version, message, attachment):
    user_ids = '['+ ', '.join(user_ids) + ']'
    s1 = f'"user_ids": {user_ids}'
    s2 = f'"access_token": "{access_token}"'
    s3 = f'"v": "{api_version}"'
    l = [s1, s2, s3]
    if message is not None:
        l.append(f'"message": "{message}"')
    if attachment is not None:
        l.append(f'"attachment": "{attachment}"')
    s = ', '.join(l)
    params = '{' + s + '}'
    return f'API.messages.send({params})'

def construct_code_for_execute(data):
    return ';'.join(data) + ';'

