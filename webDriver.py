from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
import time
import os

class UnknownKeyCommand(BaseException):
    pass

class Driver:
    def __init__(self, url, options:list=None):
        self.__url = url
        self.__custom_options = Options()
        self.__custom_options.add_argument("start-maximized")
        
        self.addOptions(options)
        
        self.__driver = webdriver.Chrome(options=self.__custom_options, service=self.__service)
        if options:
            self.Undetect()
        self.openBrowser()
        
        self.current_session = self.getCurrentSession()
        self.main_window = self.__driver.current_window_handle
    
    def Undetect(self):
        self.__driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        '''
        })
        
    def SwitchWindows(self, ind:int=None):
        if ind:
            windows = self.__driver.window_handles[ind]
        else:
            windows = self.main_window
            self.__driver.close()
        self.__driver.switch_to.window(windows)
        self.__driver.maximize_window()
        
    def SwitchFrame(self, ind:int=None):
        if ind is not None:
            self.__driver.switch_to.frame(self.__driver.find_elements(By.TAG_NAME, "iframe")[ind])
        else:
            self.__driver.switch_to.default_content()
    
    def addOptions(self, options):
        if options:
            for option in options:
                if isinstance(option, str):
                    self.__custom_options.add_argument(option)
                elif isinstance(option, tuple):
                    self.__custom_options.add_experimental_option(option[0], option[1])
            
            self.__service = Service(log_path=os.devnull)
        else:
            self.__service = None
            
    def ExecuteJS(self, code: str):
        self.__driver.execute_script(code)
        
    def getCookies(self):
        return self.__driver.get_cookies()
    
    def addCookies(self): 
        for cookie in self.getCookies():
            self.__driver.add_cookie(cookie)
        self.__driver.refresh()
    
    def WebChill(self, timeout):
        self.__driver.implicitly_wait(timeout)   
    
    def getPageTitle(self):
        return self.__driver.title
    
    def getUrl(self):
        return self.__driver.current_url
    
    def getCurrentSession(self):
        return self.__driver.session_id
    
    def openBrowser(self, url=None):
        if url:
            self.__driver.get(url)
        else:
            self.__driver.get(self.__url)
        
    def closeBrowser(self):
        self.__driver.quit()
        
    def OpenLink(self, element_path:str, ind:int=-1):
        elems = self.__driver.find_elements(By.XPATH, element_path)
        print(elems)
        elems[ind].click()
        
        
    def InputDataIntoForm(self, elemet_path:str, *input_data:str):
        search = self.__driver.find_element(By.XPATH, elemet_path)
        search.clear()
        search.send_keys(*input_data)
        search.send_keys(Keys.RETURN)
            
    def SendKeys(self, command):
        body = self.__driver.find_element(By.TAG_NAME, 'body')
        if command == 'RETURN':
            body.send_keys(Keys.RETURN)
        elif command == 'ALT+ARROW_LEFT':
            body.send_keys(Keys.ALT, Keys.ARROW_LEFT)
        elif command == 'ALT+ARROW_RIGHT':
            body.send_keys(Keys.ALT, Keys.ARROW_RIGHT)
        elif command == 'F5':
            self.__driver.refresh()
        elif command == 'ESCAPE':
            body.send_keys(Keys.ESCAPE)
        else:
            raise UnknownKeyCommand(f'You send the unknown key - {command}')
    
    def FindElementText(self, xpath:list):
        element = self.__driver.find_element(By.TAG_NAME, 'body')
        for path in xpath:
            if isinstance(path, str):
                element = element.find_elements(By.XPATH, path)[-1]
            else:
                print(element.text, element.tag_name, element.parent)
                element.click()
                
        
        return element.text  
    
    def CompleteScript(self, actions:dict, input_data:dict=None, timesleep=None):
        '''
            This method complete the handwrite script in args that
            you send to this method.
            Rules:
                1. Actions should have keywords (click, input, key, chill)
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
                    'clickAction1': 'element_path1',
                    'clickAction2': 'element_path2',
                    'InPUt1': 'element_path3',
                    'Chill': time (in seconds)
                    'AgainINPUT': 'element_path4'
                    'KEYs': 'RETURN'
                },
                {
                    'InPUt1': input_data1,
                    'AgainINPUT': input_data2
                }
            )    
        '''
        for key, value in actions.items():
            self.WebChill(5)
            if 'click' in key.lower():
                try:
                    self.OpenLink(value[0], value[1])
                except StaleElementReferenceException:
                    self.SendKeys('F5')
                    self.OpenLink(value[0], value[1])
                except ElementClickInterceptedException:
                    time.sleep(1)
                    self.OpenLink(value[0], value[1])
            elif 'input' in key.lower():
                if timesleep:
                    time.sleep(timesleep)
                    
                self.InputDataIntoForm(value, input_data[key])
            elif 'key' in key.lower():
                self.SendKeys(value.upper())
            elif 'chill' in key.lower():
                time.sleep(value)
            
    def GetUserInfo(self):
        name = self.__driver.find_element(By.XPATH, '//a[@jslog="164890;metadata:W1tudWxsLG51bGwsWzEwMDkwXV1d; track:click"]').find_element(By.CLASS_NAME, 'bJCr1d').text
        birth = self.__driver.find_element(By.XPATH, '//a[@href="birthday"]').find_element(By.CLASS_NAME, 'bJCr1d').text
        reserve = self.__driver.find_element(By.XPATH, '//a[@href="email"]').find_elements(By.CLASS_NAME, 'bJCr1d')[1].text
            
        return name, birth, reserve