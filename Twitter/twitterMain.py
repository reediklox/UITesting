import Twitter.gpt as gpt
import Twitter.twitterData as twitter
from webDriver import Driver
from JSON.jsonWork import JWork
from GoogleMail.gmailMain import getVerifyCode
from time import sleep


def homePageReturn():
    main_driver.OpenLink('//a[@href="/home"]', -1)
    
def twitterAuth(main_driver: Driver):
    main_driver.CompleteScript(
    {
        'inputUserName': '//input[@autocomplete="username"]',
        'inputPassword': '//input[@autocomplete="current-password"]'
    },
    {
        'inputUserName': twitter.LOGIN,
        'inputPassword': twitter.PASSWORD
    })
    
    sleep(2)
    checkVerification(main_driver)
    
def checkVerification(main_driver: Driver):
    if main_driver.getPageTitle() == 'Вход в X / X':
        main_driver.InputDataIntoForm('//input', getVerifyCode(
                        '//table[@style="padding:0;margin:0;line-height:1px;font-size:1px"]',
                        '//td[@style="padding:0;margin:0;line-height:1px;font-size:1px;font-family:\'HelveticaNeue\',\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:32px;line-height:36px;font-weight:bold;color:#292f33;text-align:left;text-decoration:none"]'
                    ))
    
def twitterPasswordChange():
    main_driver.CompleteScript(
        {
            'moreMenuClick': ['//div[@aria-label="More menu items"]', -1],
            'settingsClick': ['//a[@href="/settings"]', -1],
            'passwordClick': ['//a[@href="/settings/password"]', -1],
            'currentPasswordInput': '//input[@name="current_password"]',
            'newPasswordInput': '//input[@name="new_password"]',
            'confirmPasswordInput': '//input[@name="password_confirmation"]',
            'saveClick': ['//div[@data-testid="settingsDetailSave"]', -1]
        },
        {
            'currentPasswordInput': twitter.PASSWORD,
            'newPasswordInput': twitter.NEW_PASSWORD,
            'confirmPasswordInput': twitter.NEW_PASSWORD
        }
    )
    JWork.ChangePass(twitter.PATH_JSON, twitter.NEW_PASSWORD, twitter.KEY_JSON)

def NewTwit():
    homePageReturn()
    TWIT = gpt.GetRandomTwit()
    main_driver.CompleteScript(
        {
            'TwitTextInput': '//div[@role="textbox"]',
            'PostClick': ['//div[@data-testid="tweetButtonInline"]', -1]
        },
        {
            'TwitTextInput': TWIT
        }
    )



if __name__ == '__main__':
    main_driver = Driver(twitter.PATH_TWITTER)
    main_driver.WebChill(10)

    main_driver.OpenLink('//a[@href="/login"]', -1)
    twitterAuth(main_driver)
    
    
    twitterPasswordChange()
    NewTwit()

    main_driver.closeBrowser()