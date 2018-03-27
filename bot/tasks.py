import os
import redis
from celery import shared_task
from .models import Hashtag, History
from django.db.models import Q
from celery.exceptions import Ignore
from .parsers import parse_redis_data
from .vk_helpers import (
    send_execute_request, 
    construct_vkscript_message_sender, 
    construct_code_for_execute
)


@shared_task(ignore_result=True)
def handle_message_without_hashtag(message_type, date, user_id, message):
    History.save_message(message_type, date, user_id, message)

@shared_task
def handle_message_with_hashtag(message_type, date, user_id, message, hashtag):
    try:
        hashtag_obj = Hashtag.objects.get(name=hashtag)
    except DoesNotExist:
        History.save_message(message_type, date, user_id, message)
        raise Ignore
    History.save_message(message_type, date, user_id, message, hashtag_obj)
    return {'user_id': user_id, 'date': date, 'hashtag': hashtag}

@shared_task(ignore_result=True)
def send_hashtag_data():
    host = os.environ['CELERY_REDIS_HOST']
    port = os.environ['CELERY_REDIS_PORT']
    db = os.environ['CELERY_REDIS_DB']
    access_token = os.environ['VK_GROUP_ACCESS_TOKEN']
    api_version = os.environ['VK_API_VERSION']
    redis_db = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
    parsed_data = parse_redis_data(redis_db, 25, 100, 2500)
    if parsed_data is None:
        raise Ignore
    data = parsed_data['data']
    result = []
    for hashtag in data:
        message, attachment = Hashtag.get_hashtag_fields(hashtag)
        func = construct_vkscript_message_sender(
            data[hashtag], 
            access_token, 
            api_version, 
            message, 
            attachment
        )
        result.append(func)
    code = construct_code_for_execute(result)
    send_execute_request(code, access_token, api_version)
    for k in parsed_data['checked_keys']:
        redis_db.delete(k)






