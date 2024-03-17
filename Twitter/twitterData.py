from JSON.jsonWork import JWork

PATH_TWITTER = 'https://twitter.com/'

PATH_JSON = 'Data/userdata.json'
PATH_JSON_NEW = 'Data/newUserData.json'
KEY_JSON = 'Twitter'

PASSWORD = JWork.getData(KEY_JSON, PATH_JSON)['password']
LOGIN = JWork.getData(KEY_JSON, PATH_JSON)["login"]
NEW_PASSWORD = JWork.getData(KEY_JSON, PATH_JSON_NEW)['password']

API_KEY = 'DQYKw77MbuypWkAW7KpO4OdY1'
API_KEY_SECRET = '20foEE3R3Lv8pFaXQ5KZ5TW2ej3KahG7lSGu6Mj66Q9v8joydQ'
ACCESS_TOKEN = '1767992222421553152-D5F3eIzUZvylmRn63lMVXyWeyfQjhw'
ACCESS_TOKEN_SECRET = 'ACrW3RXU0gM1N4tkuu77quNx2Wl0k0dkW8ii7Blm8K8Ty'