from webDriver import Driver
from JSON.jsonWork import JWork
from time import sleep
import gpt

PATH_GMAIL = 'https://accounts.google.com/AccountChooser/signinchooser?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=AccountChooser&ec=asw-gmail-globalnav-signin'
PATH_TWITTER = 'https://twitter.com/'

PATH_JSON = 'Data/userdata.json'
PATH_JSON_NEW = 'Data/newUserData.json'
KEY_JSON = 'Twitter'

PASSWORD = JWork.getData(KEY_JSON, PATH_JSON)['password']
LOGIN = JWork.getData(KEY_JSON, PATH_JSON)["login"]
NEW_PASSWORD = JWork.getData(KEY_JSON, PATH_JSON_NEW)['password']

EMAIL_LOGIN = JWork.getData('Gmail', PATH_JSON)['login']
EMAIL_PASSWORD = JWork.getData('Gmail', PATH_JSON)['password']

def homePageReturn():
    main_driver.OpenLink('//a[@href="/home"]')

def getVerifyCode():
    gmail_driver = Driver(PATH_GMAIL)
    gmail_driver.WebChill(10)
    gmail_driver.CompleteScript(
        {
            'inputEmail': '//input[@type="email"]',
            'inputPass': '//input[@type="password"]',
            'clickLastMessage': '//tr[@jscontroller="ZdOxDb"]',           
        },
        {
            'inputEmail': EMAIL_LOGIN,
            'inputPass': EMAIL_PASSWORD
        }, 3
    )
    code = gmail_driver.FindElementText(
                [
                    '//table[@style="padding:0;margin:0;line-height:1px;font-size:1px"]',
                    '//td[@style="padding:0;margin:0;line-height:1px;font-size:1px;font-family:\'HelveticaNeue\',\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:32px;line-height:36px;font-weight:bold;color:#292f33;text-align:left;text-decoration:none"]'
                ]
            )
    
    gmail_driver.closeBrowser()
    return code
    
def twitterAuth():
    main_driver.CompleteScript(
    {
        'clickLogIn': '//a[@href="/login"]',
        'inputUserName': '//input[@autocomplete="username"]',
        'inputPassword': '//input[@autocomplete="current-password"]'
    },
    {
        'inputUserName': LOGIN,
        'inputPassword': PASSWORD
    })
    
def twitterPasswordChange():
    main_driver.CompleteScript(
        {
            'moreMenuClick': '//div[@aria-label="More menu items"]',
            'settingsClick': '//a[@href="/settings"]',
            'passwordClick': '//a[@href="/settings/password"]',
            'currentPasswordInput': '//input[@name="current_password"]',
            'newPasswordInput': '//input[@name="new_password"]',
            'confirmPasswordInput': '//input[@name="password_confirmation"]',
            'saveClick': '//div[@data-testid="settingsDetailSave"]'
        },
        {
            'currentPasswordInput': PASSWORD,
            'newPasswordInput': NEW_PASSWORD,
            'confirmPasswordInput': NEW_PASSWORD
        }
    )
    JWork.ChangePass(PATH_JSON, NEW_PASSWORD, KEY_JSON)

def NewTwit():
    homePageReturn()
    TWIT = gpt.GetRandomTwit()
    main_driver.CompleteScript(
        {
            'TwitTextInput': '//div[@role="textbox"]',
            'PostClick': '//div[@data-testid="tweetButtonInline"]'
        },
        {
            'TwitTextInput': TWIT
        }
    )

main_driver = Driver(PATH_TWITTER)
main_driver.FullSize()
main_driver.WebChill(10)
twitterAuth()
if main_driver.getPageTitle() == 'Вход в X / X':
    main_driver.InputDataIntoForm('//input', getVerifyCode())
    
twitterPasswordChange()
NewTwit()


sleep(100)
main_driver.closeBrowser()