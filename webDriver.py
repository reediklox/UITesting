from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import StaleElementReferenceException
import time
import os

class UnknownKeyCommand(BaseException):
    pass

class Driver:
    def __init__(self, url):
        self.__url = url
        self.__driver = webdriver.Chrome()
        self.__openBrowser()
    
    def WebChill(self, timeout):
        self.__driver.implicitly_wait(timeout)   
    
    def FullSize(self):
        self.__driver.set_window_size(1920, 1080)
    
    def getPageTitle(self):
        return self.__driver.title
    
    def __openBrowser(self):
            self.__driver.get(self.__url)
        
    def closeBrowser(self):
        self.__driver.quit()
        
    def OpenLink(self, element_path:str):
        self.__driver.find_element(By.XPATH, element_path).click()
        
        
    def InputDataIntoForm(self, elemet_path:str, input_data:str):
        search = self.__driver.find_element(By.XPATH, elemet_path)
        search.clear()
        search.send_keys(input_data)
        search.send_keys(Keys.RETURN)
            
    def SendKeys(self, command):
        body = self.__driver.find_element(By.TAG_NAME, 'body')
        if command == 'RETURN':
            body.send_keys(Keys.RETURN)
        elif command == 'ALT+ARROW_LEFT':
            body.send_keys(Keys.ALT + Keys.ARROW_LEFT)
        elif command == 'ALT+ARROW_RIGHT':
            body.send_keys(Keys.ALT + Keys.ARROW_RIGHT)
        elif command == 'F5':
            body.send_keys(Keys.F5)
        else:
            raise UnknownKeyCommand(f'You send the unknown key - {command}')
    
    def FindElementText(self, xpath:list, ind=0):
        element = self.__driver.find_element(By.TAG_NAME, 'body')
        for path in xpath:
            if ind:
                element = element.find_elements(By.XPATH, path)[ind]
                print(element)
            else:
                element = element.find_element(By.XPATH, path)
        
        return element.text  
    
    def CompleteScript(self, actions:dict, input_data:dict=None, timesleep=None):
        '''
            This method complete the handwrite script in args that
            you send to this method.
            Rules:
                1. Actions should have keywords (click, input, key)
                in any register
                    1.1 Click - click on the button / open the link
                    1.2 Input - input data into forms
                    1.3 Keys - keyboard keys, or commands that have
                    affect on the page
                2. input_data keys should be the same as in atcions
                3. Available Keys:
                    RETURN;
                    ALT+ARROW_LEFT;
                    ALT+ARROW_RIGHT;
                    F5;
                    
            Example:
            
            CompleteScript(
                {
                    clickAction1: element_path1,
                    clickAction2: element_path2,
                    InPUt1: element_path3,
                    AgainINPUT: element_path4
                    KEYs: RETURN
                },
                {
                    InPUt1: input_data1,
                    AgainINPUT: input_data2
                }
            )    
        '''
        for key, value in actions.items():
            self.WebChill(5)
            if 'click' in key.lower():
                try:
                    self.OpenLink(value)
                except StaleElementReferenceException:
                    self.SendKeys('F5')
                    self.OpenLink(value)
            elif 'input' in key.lower():
                if timesleep:
                    time.sleep(timesleep)
                self.InputDataIntoForm(value, input_data[key])
            elif 'key' in key.lower():
                self.SendKeys(value.upper())
            
    def GetUserInfo(self):
        name = self.__driver.find_element(By.XPATH, '//a[@jslog="164890;metadata:W1tudWxsLG51bGwsWzEwMDkwXV1d; track:click"]').find_element(By.CLASS_NAME, 'bJCr1d').text
        birth = self.__driver.find_element(By.XPATH, '//a[@href="birthday"]').find_element(By.CLASS_NAME, 'bJCr1d').text
        reserve = self.__driver.find_element(By.XPATH, '//a[@href="email"]').find_elements(By.CLASS_NAME, 'bJCr1d')[1].text
            
        return name, birth, reserve