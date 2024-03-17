from JSON.jsonWork import JWork

PATH_GALXE = 'https://galxe.com/'

PATH_JSON = 'Data/userdata.json'
PATH_JSON_NEW = 'Data/newUserData.json'
KEY_JSON = 'Galxe'

FOLLOW_SPACES = [f'//div[contains(@class, "space-box position-relative space-box-") and .//a[@href="{space}"]]//span[@class="status-text" and text()="+ Follow"]' for space in JWork.getData(KEY_JSON, PATH_JSON)['spaces']]

LOGIN = JWork.getData(KEY_JSON, PATH_JSON)['login']
NEW_USERNAME = JWork.getData(KEY_JSON, PATH_JSON_NEW)['name']

DISCORD_LOGIN = JWork.getData('Discord', PATH_JSON)['login']
DISCORD_PASSWORD = JWork.getData('Discord', PATH_JSON)['password']
DISCORD_TOKEN = 'MTIxODc5MTMwMTk3ODM5MDU1OA.GZPWf2.x-ENN5isRXzqWjuTtGRokarEMla6EBEYBpWHlM'
DISCORD_LOGGER = '''let token = "MTIxODc5MTMwMTk3ODM5MDU1OA.GZPWf2.x-ENN5isRXzqWjuTtGRokarEMla6EBEYBpWHlM";
                   function login(token) { 
                        setInterval(() => {
                        document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
                        }, 50);
                        setTimeout(() => {
                        location.reload();
                        }, 2500);
                    }
                    login(token);'''
                    
CAMPAIN_PATH = 'https://galxe.com/taiko/campaign/GC8TMt4fFG'