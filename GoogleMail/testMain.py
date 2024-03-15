from JSON.jsonWork import JWork
import json
import time
import threading
from webDriver import Driver
import pandas as pd


PATH_JSON = 'Data/userdata.json'
PATH_JSON_NEW = 'Data/newUserData.json'
KEY_JSON = 'Gmail'
PASSWORD = JWork.getData(KEY_JSON, PATH_JSON)['password']
LOGIN = JWork.getData(KEY_JSON, PATH_JSON)["login"]
NEW_PASSWORD = JWork.getData(KEY_JSON, PATH_JSON_NEW)['password']

AUTH_PATH = [   
                '/html/body/header/div/div/div/a[2]',
                '//*[@id="identifierId"]', 
                '//*[@id="password"]/div[1]/div/div[1]/input',
            ]
AUTH_DATA = [
                LOGIN,
                PASSWORD
            ]

TABLE = {'Email': [AUTH_DATA[0]], 'Password': [AUTH_DATA[1]], 'Name/Last Name': None, 'Birth Date': None, 'Reserve Email': None}

def GmailAuth(driver:Driver, path:list):
    driver.CompleteScript(
        {
            'LoginClick': path[0],
            'InputEmail': path[1],
            'InputPassword': path[2],
        },
        {
            'InputEmail': LOGIN,
            'InputPassword': PASSWORD
        }, 3)

def RunThread(url, page_name):
    if page_name == 'personal_info':
        person_driver = Driver(url)
        GmailAuth(person_driver, ['//a[@aria-label="Войти"]', '//input[@type="email"]', '//input[@type="password"]'])       
        
        person_driver.CompleteScript(
            {
                'NameClick': '//a[@href="profile/name?continue=https%3A%2F%2Fmyaccount.google.com%2Fpersonal-info"]',
                'EditNameClick': '//button[@aria-label="Edit Name"]',
                'InputName': '//input[@id="i6"]',
                'InputLastName': '//input[@id="i11"]',
                'SaveClick': '//button[@class="UywwFc-LgbsSe UywwFc-LgbsSe-OWXEXe-dgl2Hf wMI9H"]'
            },
            {
                'InputName': JWork.getData(KEY_JSON, PATH_JSON_NEW)['name'],
                'InputLastName': JWork.getData(KEY_JSON, PATH_JSON_NEW)['lastname']
            }
        )

        person_driver.closeBrowser()       
    elif page_name == 'security':
        
        sec_driver = Driver(url)
        GmailAuth(sec_driver, ['//a[@aria-label="Войти"]', '//input[@type="email"]', '//input[@type="password"]'])
        
        sec_driver.CompleteScript(
            {
                'PassClick': '//*[@aria-label="Password"]',
                'InputNewPass': '//*[@id="i5"]',
                'InputConfirm':'//*[@id="i11"]'
            },
            { 
                'InputNewPass': NEW_PASSWORD,
                'InputConfirm': NEW_PASSWORD
            })
        
        JWork.ChangePass(PATH_JSON, NEW_PASSWORD, KEY_JSON)
        global PASSWORD 
        PASSWORD = NEW_PASSWORD
        
        sec_driver.closeBrowser()


urls = ['https://myaccount.google.com/personal-info', 'https://myaccount.google.com/security']
actions = ['personal_info', 'security']

thread1 = threading.Thread(target=RunThread, args=(urls[0], actions[0], ))
thread2 = threading.Thread(target=RunThread, args=(urls[1], actions[1], ))
    
thread1.start()
thread2.start()

thread1.join()
thread2.join()

person_driver = Driver(urls[0])
GmailAuth(person_driver, ['//a[@aria-label="Войти"]', '//input[@type="email"]', '//input[@type="password"]'])

NAME, BIRTH, RESERVE = person_driver.GetUserInfo()
person_driver.closeBrowser()

TABLE['Password'] = [PASSWORD]
TABLE['Name/Last Name'] = [NAME]
TABLE['Birth Date'] = [BIRTH]
TABLE['Reserve Email'] = [RESERVE]

df = pd.DataFrame(TABLE)
df.to_excel('GoogleMail/Gmail.xlsx')