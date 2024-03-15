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


def RunThread(url, page_name):
    if page_name == 'personal_info':
        person_driver = Driver(url)
        person_driver.OpenLink('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[3]/div/div/c-wiz/section/div/div/div/div/div/div/header/div[3]/div/div/a')
        person_driver.Authorithation(AUTH_PATH, AUTH_DATA)
        
        person_driver.ChangeUserInfo([
            '//*[@jslog="164890;metadata:W1tudWxsLG51bGwsWzEwMDkwXV1d; track:click"]',
            '//button[@aria-label="Edit Name"]',
            '//*[@id="i6"]',
            '//*[@id="i11"]',
            '//button[@class="UywwFc-LgbsSe UywwFc-LgbsSe-OWXEXe-dgl2Hf wMI9H"]'
        ],
        [
            JWork.getData(KEY_JSON, PATH_JSON_NEW)['name'],
            JWork.getData(KEY_JSON, PATH_JSON_NEW)['lastname']
        ])
        time.sleep(5)
        person_driver.closeBrowser()
    elif page_name == 'security':
        sec_driver = Driver(url)
        sec_driver.OpenLink('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[3]/div/div/c-wiz/section/div/div/div/div/div/div/header/div[3]/div/div/a')
        sec_driver.Authorithation(AUTH_PATH, AUTH_DATA)
        sec_driver.ChangePassword([
            '//*[@aria-label="Password"]',
            '//*[@id="i5"]',
            '//*[@id="i11"]',
            '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/c-wiz/div/div[4]/form/div/div[2]/div/div/button'
        ], 
            NEW_PASSWORD)
        JWork.ChangePass(PATH_JSON, NEW_PASSWORD, KEY_JSON)
        sec_driver.closeBrowser()


main_driver = Driver('https://www.google.com/intl/ru/gmail/about/')
main_driver.Authorithation(AUTH_PATH, AUTH_DATA, True)

urls = ['https://myaccount.google.com/personal-info', 'https://myaccount.google.com/security']
actions = ['personal_info', 'security']

thread1 = threading.Thread(target=RunThread, args=(urls[0], actions[0], ))
thread2 = threading.Thread(target=RunThread, args=(urls[1], actions[1], ))
    
thread1.start()
thread2.start()

thread1.join()
thread2.join()

person_driver = Driver(urls[0])
person_driver.Authorithation(AUTH_PATH, [LOGIN, NEW_PASSWORD])
NAME, BIRTH, RESERVE = person_driver.GetUserInfo()
person_driver.closeBrowser()

TABLE['Password'] = [NEW_PASSWORD]
TABLE['Name/Last Name'] = [NAME]
TABLE['Birth Date'] = [BIRTH]
TABLE['Reserve Email'] = [RESERVE]

df = pd.DataFrame(TABLE)
df.to_excel('GoogleMail/Gmail.xlsx')

main_driver.closeBrowser()
