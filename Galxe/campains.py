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
                Follow: username,
                Like: post_id,
                Retweet: post_id
            }
    '''
    auth = tweepy.OAuth1UserHandler(twitter.API_KEY, twitter.API_KEY_SECRET, twitter.ACCESS_TOKEN, twitter.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    
    for action, value in actions.items():
        if 'follow' in action.lower():
            api.create_friendship(screen_name=value)
        elif 'like' in action.lower():
            api.create_favorite(id=value)
        elif 'retweet' in action.lower():
            api.retweet(id=value)
            

def VisitWebSiteComlete(url):
    responce = requests.get(url)
    
    if responce.status_code == 200:
        return True
    else: 
        return False

