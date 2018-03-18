import time
from celery import shared_task
import requests
from .models import Vgroup, Hashtag, History
from django.db.models import Q

# timesleep = 9 seconds
def send_message(user_id, access_token, api_version, message, attachment):
    if not message and not attachment:
        return None
    time.sleep(2)
    url_send_message = 'https://api.vk.com/method/messages.send'
    params = {
        'user_id': user_id,
        'access_token': access_token,
        'v': api_version
    }
    if message:
        params['message'] = message
    if attachment:
        params['attachment'] = attachment      
    requests.get(url_send_message, params=params)


@shared_task(ignore_result=True)
def reply_to_message(user_id, access_token, api_version, group_id, hashtag):
    hashtag = Hashtag.objects.select_related().filter(Q(name=hashtag) & Q(group__id=group_id)).first()
    if hashtag is not None:
        send_message(
            user_id,
            access_token,
            api_version,
            hashtag.message,
            hashtag.attachment   
        )


@shared_task(ignore_result=True)
def save_message(data, hashtag):
    group_id = data['group_id']
    group = Vgroup.objects.get(pk=group_id)
    history = History(
        message_type=data['message_type'],
        date=data['date'],
        user_id=data['user_id'],
        message=data['message'],
        group=group
    )
    if hashtag is not None:
        hashtag = Hashtag.objects.filter(Q(name=hashtag) & Q(group__id=group_id)).first()
        if hashtag is not None:
            history.hashtag = hashtag
    history.save()