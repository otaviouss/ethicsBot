from platform import python_version
from asyncio.log import logger
from dotenv import load_dotenv
from math import inf
from os import times
import requests
import tweepy
import os

class EthicsListener(tweepy.Stream):

    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret, api, *, chunk_size=512, daemon=False,
                 max_retries=inf, proxy=None, verify=True):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.chunk_size = chunk_size
        self.daemon = daemon
        self.max_retries = max_retries
        self.proxies = {"https": proxy} if proxy else {}
        self.verify = verify

        self.running = False
        self.session = None
        self.thread = None
        self.user_agent = (
            f"Python/{python_version()} "
            f"Requests/{requests.__version__} "
            f"Tweepy/{tweepy.__version__}"
        )

        self.api = api
        self.stats_json = dict()

    def on_status(self, status):
        '''
        Tweet the result of the analysis executed by pegabot
        Parameters:
            status (string): 
        Returns:
            total (int): Result (total analysis)
        '''

        ## Filters ##

        # If it is a retweet
        try:
            ret = status.retweeted_status
            return
        except:
            pass

        # If it is a response to another tweet
        if(str(status.in_reply_to_status_id) != "None"):
            return
        
        # If it is a quotation
        try:
            i = status.quoted_status_id
            return
        except:
            pass

        # Related Terms
        if (
            status.text.find("computation")  != -1 or status.text.find("computação")     != -1 or
            status.text.find("computing")    != -1 or 
            status.text.find("social media") != -1 or status.text.find("redes sociais")  != -1 or
            status.text.find("software")     != -1 or 
            status.text.find("algorithm")    != -1 or status.text.find("algoritmo")      != -1 or
            status.text.find("algorithms")   != -1 or 
            status.text.find("tecnology")    != -1 or status.text.find("tecnologia")     != -1 or
            status.text.find(" tech")        != -1 or
            status.text.find("intenet")      != -1 or
            status.text.find("AI")           != -1 or
            status.text.find("artificial inteligence")    != -1 or status.text.find("inteligência artificial")  != -1 or
            status.text.find("software engineering")      != -1 or status.text.find("engenharia de software")   != -1 or
            status.text.find("requirements engineering")  != -1 or status.text.find("engenharia de requisitos") != -1
            ):
                    pass
        else:
            return

        print(status.text)
        if not status.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                self.api.retweet(status.id)
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

        # print('Username: ' + status.user.screen_name)
        # print(status.text)

    def on_limit(self,status):
        # Rate Limit Exceeded, Sleep for 15 Mins
        times.sleep(15 * 60)
        return True

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            print(status_code)
            return False

        
def listen(string_list = [""]):
    
    load_dotenv()
    
    auth = tweepy.OAuthHandler(
            os.environ.get('CONSUMER_KEY'),
            os.environ.get('CONSUMER_SECRET')
            )
    auth.set_access_token(
            os.environ.get('ACCESS_TOKEN'),
            os.environ.get('ACCESS_TOKEN_SECRET')
            )
    
    api = tweepy.API(auth)

    ethics_listener = EthicsListener(auth.consumer_key, auth.consumer_secret, auth.access_token, auth.access_token_secret, api)
    
    ethics_listener.filter(track=string_list) # Define which strings to watch
    
    ethics_listener.sample() # Start the stream


if __name__ == "__main__":
    listen(string_list = ["ethics", "ethicaly", "ética", "morally", "privacy", "#ethicsBot", "#botEtico"])
