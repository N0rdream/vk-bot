import json
import os
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from .tasks import reply_to_message, save_message
from vk_bot_prj.config import load_config
import re 


def get_hashtag(text):
	pattern = re.compile(r'(?<=#)\w+')
	hashtag = pattern.findall(text)
	if hashtag:
		return hashtag[0].lower()


def process_json(data):
	# exception handling
	# except KeyError
	message_type = data['type']
	secret = data['secret']
	group_id = data['group_id']
	result =  {
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


@csrf_exempt
@require_http_methods(['POST'])
def main(request):
	config = load_config(os.environ['VK_CONFIG'])
	json_data = json.loads(request.body)
	print(json_data)
	data = process_json(json_data)
	print(data)
	group_id = str(data['group_id'])
	message_type = data['message_type']
	if group_id in config['groups']:
		group = config['groups'][group_id]
		if data['secret'] == group['secret_key']:
			if message_type == 'confirmation':
				return HttpResponse(group['confirmation'])
			if message_type in ['message_new', 'message_edit']:
				hashtag = get_hashtag(data['message'])
				save_message.delay(data, hashtag)
				if hashtag is not None:
					reply_to_message.delay(
						data['user_id'],
						group['access_token'],
						config['api_version'],
						data['group_id'],
						hashtag
					)
				return HttpResponse('ok', status=200)

