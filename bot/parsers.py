import re
import json


def get_hashtag_from_message(message):
    pattern = re.compile(r'(?<=#)\w+')
    hashtag = pattern.findall(message)
    if hashtag:
        return hashtag[0].lower()

def process_incoming_data(data):
    try:
        message_type = data['type']
        secret = data['secret']
        group_id = data['group_id']
    except (KeyError, TypeError):
        return None
    result = {
        'message_type': message_type,
        'group_id': group_id,
        'secret': secret
    }
    try:
        vk_timestamp = data['object']['date']
        user_id = data['object']['user_id']
        message = data['object']['body']
    except KeyError:
        return result
    else:
        result['vk_timestamp'] = vk_timestamp
        result['message'] = message
        result['user_id'] = user_id
    return result

def parse_redis_data(redis_data, execute_limit=25, user_ids_limit=100):
    redis_keys = redis_data.keys()
    if not redis_keys:
        return None
    data = {}
    checked_keys = set()
    for redis_key in redis_keys:
        record = json.loads(redis_data.get(redis_key))
        try:
            message = record['result']['message']
            vk_attachment_id = record['result']['vk_attachment_id']
            user_id = record['result']['user_id']
        except (KeyError, TypeError):
            checked_keys.add(redis_key)
            continue
        the_key = (message, vk_attachment_id)
        if the_key not in data:
            if len(data) < execute_limit:
                data[the_key] = {user_id}
                checked_keys.add(redis_key)
        else:
            if len(data[the_key]) < user_ids_limit:
                data[the_key].add(user_id)
                checked_keys.add(redis_key)
    return {
        'data': data, 
        'checked_keys': checked_keys
    }




