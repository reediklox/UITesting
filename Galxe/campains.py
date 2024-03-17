import requests
import tweepy
from time import sleep
from Galxe import galxeData as galxe
from bs4 import BeautifulSoup
from Twitter import twitterData as twitter

def TwitterChallenges(actions:dict):
    '''
        Example of actions:

            actions = {
                Follow: @username,
                Like: post_id,
                Retweet: post_id
            }
    '''
    auth = tweepy.OAuth1UserHandler(twitter.API_KEY, twitter.API_KEY_SECRET, twitter.ACCESS_TOKEN, twitter.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    
    for action, value in actions.items():
        if 'follow' in action.lower():
            api.create_friendship(user_id=value)
        elif 'like' in action.lower():
            api.create_favorite(id=value)
        elif 'retweet' in action.lower():
            api.retweet(id=value)
            
            
            
def redirection(campains_url: str, cookies):
    session = requests.Session()
    
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
        
    responce = session.get(campains_url)
    
    print(responce.headers)
    
    sleep(4)
    if responce.status_code == 200:
        html = responce.text
        
        soup = BeautifulSoup(html, 'html.parser')
        #print(soup.prettify())
        
        list_container = soup.findAll('div', class_='campaign-container bg-lighten-1 d-flex list-mode-item')
        print(list_container)
        
        if list_container:
            print('Successfuly find a button: ', list_container)
        
        else:
            print('Button cant be founded!')
            
    else:
        print('Respone cant be geted!')
    
    sleep(100)

