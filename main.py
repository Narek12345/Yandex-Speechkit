from fastapi import FastAPI
from fastapi import UploadFile, File

import json
import requests

app = FastAPI()

# Data for connecting to Yandex Cloud.
URL = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'
folder_id = "b1goutam1lu7mrpga53k"
oauth_token = "y0_AgAAAAAE2_2tAATuwQAAAADyV6oXjMC0QTPRQhu7ZyDegvmNsI6tKWw"


def create_token(oauth_token):
	params = {'yandexPassportOauthToken': oauth_token}
	response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', params=params)                                                   
	decode_response = response.content.decode('UTF-8')
	text = json.loads(decode_response) 
	iam_token = text.get('iamToken')

	return iam_token


@app.post('/speech_recognition')
async def speech_recognition(file: UploadFile):
	"""We receive a .ogg file, which we then send to Yandex Cloud for speech recognition, then we send the resulting text back."""

	iam_token = create_token(oauth_token)

	headers = {'Authorization': f'Bearer {iam_token}'}

	params = {
		'lang': 'ru-RU',
		'format': 'oggopus',
		'sampleRateHertz': 48000,
		'folderId': folder_id,
	}

	response = requests.post(URL, params=params, headers=headers, data=file.file.read())

	decode_resp = response.content.decode('UTF-8')

	text = json.loads(decode_resp)
	
	return text
