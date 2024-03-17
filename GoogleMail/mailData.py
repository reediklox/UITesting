from JSON.jsonWork import JWork

PATH_GMAIL = 'https://accounts.google.com/AccountChooser/signinchooser?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=AccountChooser&ec=asw-gmail-globalnav-signin'

PATH_JSON = 'Data/userdata.json'
PATH_JSON_NEW = 'Data/newUserData.json'
KEY_JSON = 'Gmail'

PASSWORD = JWork.getData(KEY_JSON, PATH_JSON)['password']
LOGIN = JWork.getData(KEY_JSON, PATH_JSON)["login"]
NEW_PASSWORD = JWork.getData(KEY_JSON, PATH_JSON_NEW)['password']

TABLE = {'Email': [LOGIN], 'Password': [PASSWORD], 'Name/Last Name': None, 'Birth Date': None, 'Reserve Email': None}