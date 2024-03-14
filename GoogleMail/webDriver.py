from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
import time


class Driver:
    def __init__(self, url):
        self.__url = url
        self.__driver = webdriver.Chrome()
        self.__openBrowser()
        self.__initial_title = self.__driver.title
        
    def __openBrowser(self):
            self.__driver.get(self.__url)
        
    def closeBrowser(self):
        self.__driver.quit()
        
    def InputDataIntoForm(self, elemet_path:str, input_data:str):
        search = self.__driver.find_element(By.XPATH, elemet_path)
        search.clear()
        search.send_keys(input_data)
        search.send_keys(Keys.RETURN)
        
    def InputNewPassword(self, input_data):
        self.__driver.implicitly_wait(3)
        self.__driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.RETURN)
        self.__driver.implicitly_wait(2)
        search = self.__driver.find_element(By.XPATH, '//input[@autocomplete="current-password"]')
        search.send_keys(input_data)
        search.send_keys(Keys.RETURN)
        for i in range(4):
            self.__driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ALT + Keys.ARROW_LEFT)
            
            
    def OpenLink(self, element_path:str):
        search = self.__driver.find_element(By.XPATH, element_path)
        search.click()
        
    def Authorithation(self, element_path:list, input_data:list, main_auth:bool=False):
        if main_auth:
            self.OpenLink(element_path[0])
        else:
            self.OpenLink(element_path[1]) # Open the auth page
        self.InputDataIntoForm(element_path[2], input_data[0]) # Input the gmail
        self.__driver.implicitly_wait(5) # Chill until the pass input page does not open
        self.InputDataIntoForm(element_path[3], input_data[1]) # Input the password
        self.__driver.implicitly_wait(5) # Chill again until the idk...general? page does not open
        
    def ChangePassword(self, element_path:list, new_password:str):
        self.OpenLink(element_path[0]) # Open the change pass page
        self.InputDataIntoForm(element_path[1], new_password) # Input new password
        time.sleep(1)
        self.InputDataIntoForm(element_path[2], new_password) # Confirm password
        
    def ChangeUserInfo(self, element_path:list, new_data:list):
        self.OpenLink(element_path[0]) # Open the change personal info page
        self.__driver.implicitly_wait(2)
        self.OpenLink(element_path[1]) # Open the name change page
        self.InputDataIntoForm(element_path[2], new_data[0]) # Change name
        self.InputDataIntoForm(element_path[3], new_data[1]) # Change lastname
        self.OpenLink(element_path[4])
    
    def GetUserInfo(self):        
        name = self.__driver.find_element(By.XPATH, '//a[@jslog="164890;metadata:W1tudWxsLG51bGwsWzEwMDkwXV1d; track:click"]').find_element(By.CLASS_NAME, 'bJCr1d').text
        birth = self.__driver.find_element(By.XPATH, '//a[@href="birthday"]').find_element(By.CLASS_NAME, 'bJCr1d').text
        reserve = self.__driver.find_element(By.XPATH, '//a[@href="email"]').find_elements(By.CLASS_NAME, 'bJCr1d')[1].text
        
        return name, birth, reserve