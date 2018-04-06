import json
import os
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from .tasks import handle_message_without_hashtag, handle_message_with_hashtag
from .parsers import get_hashtag_from_message, process_incoming_data


@csrf_exempt
@require_http_methods(['POST'])
def handle_request(request):
    json_data = json.loads(request.body)
    data = process_incoming_data(json_data)
    if data is None:
        return HttpResponse('Invalid incoming data', status=400)
    message_type = data['message_type']
    message = data['message']
    vk_timestamp = data['vk_timestamp']
    user_id = data['user_id']
    if data['secret'] != os.environ['VK_GROUP_SECRET_KEY']:
        return HttpResponse('Invalid secret key', status=403) 
    if message_type == 'confirmation':
        return HttpResponse(os.environ['VK_GROUP_CONFIRMATION'])
    if message_type == 'message_new' or message_type =='message_edit':
        hashtag = get_hashtag_from_message(message)
        if hashtag is None:
            handle_message_without_hashtag.delay(
                message_type, vk_timestamp, user_id, message
            )
        else:
            handle_message_with_hashtag.delay(
                message_type, vk_timestamp, user_id, message, hashtag
            )
    return HttpResponse('ok', status=200)
