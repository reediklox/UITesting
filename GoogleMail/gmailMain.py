import threading
import pandas as pd
import GoogleMail.mailData as mail
from webDriver import Driver
from JSON.jsonWork import JWork
import os


def getVerifyCode(*elements) -> str:
    gmail_driver = Driver(mail.PATH_GMAIL)
    gmail_driver.WebChill(10)
    gmail_driver.CompleteScript(
        {
            'inputEmail': '//input[@type="email"]',
            'inputPass': '//input[@type="password"]',
            'Chill': 15,
            'F5Key': 'F5',
            'Chill': 2,
            'clickLastMessage': ['//tr[@jscontroller="ZdOxDb"]', 0],           
        },
        {
            'inputEmail': mail.LOGIN,
            'inputPass': mail.PASSWORD
        }, 3
    )
    
    code = gmail_driver.FindElementText(
                elements
            )
    
    gmail_driver.closeBrowser()
    return code

def GmailAuth(driver:Driver, path:list):
    driver.CompleteScript(
        {
            'LoginClick': [path[0], -1],
            'InputEmail': path[1],
            'InputPassword': path[2],
        },
        {
            'InputEmail': mail.LOGIN,
            'InputPassword': mail.PASSWORD
        }, 3)

def RunThread(url, page_name):
    if page_name == 'personal_info':
        person_driver = Driver(url)
        GmailAuth(person_driver, ['//a[@aria-label="Войти"]', '//input[@type="email"]', '//input[@type="password"]'])       
        
        person_driver.CompleteScript(
            {
                'NameClick': ['//a[@href="profile/name?continue=https%3A%2F%2Fmyaccount.google.com%2Fpersonal-info"]', -1],
                'EditNameClick': ['//button[@aria-label="Edit Name"]', -1],
                'InputName': '//input[@id="i6"]',
                'InputLastName': '//input[@id="i11"]',
                'SaveClick': ['//button[@class="UywwFc-LgbsSe UywwFc-LgbsSe-OWXEXe-dgl2Hf wMI9H"]', -1]
            },
            {
                'InputName': JWork.getData(mail.KEY_JSON, mail.PATH_JSON_NEW)['name'],
                'InputLastName': JWork.getData(mail.KEY_JSON, mail.PATH_JSON_NEW)['lastname']
            }
        )

        person_driver.closeBrowser()       
    elif page_name == 'security':
        
        sec_driver = Driver(url)
        GmailAuth(sec_driver, ['//a[@aria-label="Войти"]', '//input[@type="email"]', '//input[@type="password"]'])
        
        sec_driver.CompleteScript(
            {
                'PassClick': ['//*[@aria-label="Password"]', -1],
                'InputNewPass': '//*[@id="i5"]',
                'InputConfirm':'//*[@id="i11"]'
            },
            { 
                'InputNewPass': mail.NEW_PASSWORD,
                'InputConfirm': mail.NEW_PASSWORD
            })
        
        JWork.ChangePass(mail.PATH_JSON, mail.NEW_PASSWORD, mail.KEY_JSON)
        mail.PASSWORD = mail.NEW_PASSWORD
        
        sec_driver.closeBrowser()

if __name__ == '__main__':
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

    mail.TABLE['Password'] = [mail.PASSWORD]
    mail.TABLE['Name/Last Name'] = [NAME]
    mail.TABLE['Birth Date'] = [BIRTH]
    mail.TABLE['Reserve Email'] = [RESERVE]

    df = pd.DataFrame(mail.TABLE)
    df.to_excel('GoogleMail/Gmail.xlsx')