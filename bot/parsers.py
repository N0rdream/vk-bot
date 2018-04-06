import re
import json
from collections import defaultdict


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
    keys = redis_data.keys()
    if not keys:
        return None
    data = {}
    checked_keys = set()
    for k in keys:
        record = json.loads(redis_data.get(k))
        try:
            hashtag = record['result']['hashtag']
            user_id = record['result']['user_id']
        except (KeyError, TypeError):
            checked_keys.add(k)
            continue
        if hashtag not in data:
            if len(data) < execute_limit:
                data[hashtag] = {user_id}
                checked_keys.add(k)
        else:
            if len(data[hashtag]) < user_ids_limit:
                data[hashtag].add(user_id)
                checked_keys.add(k)
    return {
        'data': data, 
        'checked_keys': checked_keys
    }