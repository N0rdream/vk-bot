import requests


jdata1 = {
	'type': 'message_new',
	'object': {
		'id': 136,
		'date': 1519246275,
		'out': 0,
		'user_id': 48864524,
		'read_state': 0, 
		'title': '', 
		'body': '#test2'
	}, 
	'group_id': 159735212, 
	'secret': 'kgESe647R68IUctDR465f80YihVd66687uUHBU'
}

jdata2 = {
	'type': 'confirmation',
	'group_id': 777, 
	'secret': 'test_secret_key'
}


url1 = 'https://nordream.ru/bot/'
url2 = 'http://127.0.0.1:8000/bot/'





for i in range(150):
	jdata1['object']['body'] = '       ' + str(i) + ' #test1'
	print(i)
	r = requests.post(url1, json=jdata1)
	print(r.text)