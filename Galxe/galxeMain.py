import galxeData as galxe
from webDriver import Driver
from Twitter import twitterData as twitter
from GoogleMail import mailData as mail
from GoogleMail.gmailMain import getVerifyCode
from Twitter import twitterMain as tweet
from selenium.webdriver.common.keys import Keys
from Galxe import campains
from time import sleep


def GalxeAuthByMail():
    main_driver.CompleteScript({
        'LoginClick': ['//div[contains(text(),"Log in")]', -1],
        'EmailClick': ['//li[@class="login-item-wrapper email clickable"]', -1],
        'EmailInput': '//input[contains(@type, "email")]',
        'SendACodeClick': ['//a[contains(text(), "Send a code")]', -1],
    },
    {
        'EmailInput': galxe.LOGIN
    }, 2) # Script to send a verify code
    
    main_driver.CompleteScript({
        'CodeInput': '//input[contains(@type, "text")]',
        'LoginClick': ['//button[contains(text(), "Login")]', -1]
    },
    {
        'CodeInput': getVerifyCode('//h1')  
    }) # Input code and login

def MakeTweet():
    sleep(4)
    main_driver.openBrowser('https://galxe.com/twitterConnect')

    sleep(3)
    main_driver.OpenLink('//div[contains(text(),"Tweet")]', -1)
    main_driver.SwitchWindows(-1)
    
    main_driver.OpenLink('//span[contains(text(), "Войти")]', -1)
    
    tweet.twitterAuth(main_driver)
    
    main_driver.CompleteScript({
        'PostClick': ['//span[contains(text(), "Post")]', 0],
        'Chill': 2,
        'RefreshKey': 'F5',
        'Chill': 4,
        'EscKey': 'ESCAPE',
        'Chill': 2,
        'ProfilePageClick': ['//span[contains(text(), "Profile")]', 0],
        'Chill': 2,
        'ShareClick': ['//div[contains(@aria-label, "Share post")]', 0],
        'CopyLinkClick': ['//span[contains(text(), "Copy link")]', 0]
    })
    
    main_driver.SwitchWindows()
    
    main_driver.CompleteScript({
        'InputLink': '//input[contains(@placeholder, "Paste link here")]',
        'VerifyClick': ['//span[contains(text(), "Verify")]', -1]
    }, 
    {
        'InputLink': [Keys.CONTROL, 'v']
    })
    
def goToSettingsSocial():
    main_driver.CompleteScript({
        'ProfileImageClick': ['//div[@class="campaign-avatar-inner"]', 0],
        'UselessClick': ['//h1[contains(@class, "original text-mona-sans-bold")]', 0],
        'SettingsClick': ['//img[@class="d-inline-flex icon clickable"]', 0],
        'SocialAccountsClick': ['//div[contains(text(), "Social Accounts")]', 0]
    })

def ConnectDiscord():
    
    #goToSettingsSocial()
    sleep(2)
    
    main_driver.OpenLink('//div[contains(text(), "Connect Discord Account")]', -1)
    sleep(1)
    
    main_driver.SwitchWindows(-1)
    main_driver.ExecuteJS(galxe.DISCORD_LOGGER)
    main_driver.OpenLink('//div[contains(text(), "Авторизовать")]', -1)
    
    sleep(10)
    main_driver.SwitchWindows()
    main_driver.SendKeys('F5')
    sleep(1)
    
def ChangeUserName():
    try:
        main_driver.FindElementText(['//div[contains(text(),"Log in")]'])
        GalxeAuthByMail()
    except Exception:
        print('')
    
    sleep(2)
    goToSettingsSocial()
    sleep(2)
    
    main_driver.CompleteScript({
        'ProfileSettingsClick': ['//div[contains(text(), "Profile Setting")]', 0],
        'EnterUsernameClick': ['//input[contains(@placeholder, "Enter Username")]', 0],
        'InputClear': '//input[contains(@placeholder, "Enter Username")]',
        'InputUsername': '//input[contains(@placeholder, "Enter Username")]',
        'SaveClick': ['//span[contains(text(), "Save")]', 0]
    },
    {
        'InputClear': [Keys.CONTROL, 'a', Keys.BACKSPACE],
        'InputUsername': galxe.NEW_USERNAME
    }, 2)
    sleep(3)
    
def FollowSpaces():
    main_driver.OpenLink('//a[contains(text(), "Spaces")]', 0)
    sleep(3)
    
    print(galxe.FOLLOW_SPACES)
    
    main_driver.SendKeys('F5')
    try:
        main_driver.OpenLink('//*[contains(@class, "icon-close")]', -1)
    except Exception:
        print('Element is not found')
        
    for space in galxe.FOLLOW_SPACES:
        sleep(2)
        main_driver.FindElementText([
                space,
                1
            ])

def CompliteCampains():
    sleep(2)
    main_driver.openBrowser(galxe.CAMPAIN_PATH)
    
    cookies = main_driver.getCookies()
    url = main_driver.getUrl()
    
    campains.redirection(url, cookies)
    

options = ["--disable-blink-features=AutomationControlled"]
main_driver = Driver(galxe.PATH_GALXE, options)

GalxeAuthByMail() #Done

# MakeTweet() #Done
# ConnectDiscord() #Done
# ChangeUserName() # Done
# FollowSpaces() # Done

CompliteCampains()

sleep(10)
main_driver.closeBrowser()