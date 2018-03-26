import json
import os
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from .tasks import store_incoming_message
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
    if data['secret'] != os.environ['VK_GROUP_SECRET_KEY']:
        return HttpResponse('Invalid secret key', status=403) 
    if message_type == 'confirmation':
        return HttpResponse(os.environ['VK_GROUP_CONFIRMATION'])
    if message_type == 'message_new' or message_type =='message_edit':
        hashtag = get_hashtag_from_message(message)
        store_incoming_message.delay(
            message_type,
            data['date'],
            data['user_id'],
            message,
            hashtag
        )
    return HttpResponse('ok', status=200)
