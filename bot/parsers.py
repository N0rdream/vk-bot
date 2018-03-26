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
    except KeyError:
        return None
    result = {
        'message_type': message_type,
        'group_id': group_id,
        'secret': secret
    }
    try:
        date = data['object']['date']
        user_id = data['object']['user_id']
        message = data['object']['body']
    except KeyError:
        return result
    else:
        result['date'] = date
        result['message'] = message
        result['user_id'] = user_id
    return result

def parse_redis_data(redis_data, execute_limit, user_ids_limit, slice_size):
    keys = redis_data.keys()[:slice_size]
    if not keys:
        return None
    data = {}
    checked_keys = []
    broken_keys = []
    for k in keys:
        record = json.loads(redis_data.get(k))
        try:
            hashtag = record['result']['hashtag']
            user_id = str(record['result']['user_id'])
        except KeyError:
            broken_keys.append(k)
            continue
        if hashtag not in data:
            if len(data) < execute_limit:
                data[hashtag] = [user_id]
                checked_keys.append(k)
        else:
            if len(data[hashtag]) < user_ids_limit:
                data[hashtag].append(user_id)
                checked_keys.append(k)
    return {
        'data': data, 
        'checked_keys': checked_keys, 
        'broken_keys': broken_keys
    }