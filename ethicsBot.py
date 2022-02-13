from asyncio.log import logger
from deep_translator import GoogleTranslator
from platform import python_version
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
        self.last_tweet = "null"

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

        st = status
        try:
            status = self.api.get_status(status.id_str, tweet_mode="extended")
        except:
            return
            
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

        # Non Desired Terms
        if(
            status.full_text.find("deal")      != -1 or
            status.full_text.find("Deal")      != -1 or
            status.full_text.find("promotion") != -1 or
            status.full_text.find("Promotion") != -1 or
            status.full_text.find("download")  != -1 or
            status.full_text.find("Download")  != -1 or
            status.full_text.find("sale")      != -1 or
            status.full_text.find("Sale")      != -1 or
            status.full_text == self.last_tweet
        ):
            return

        # Related Terms
        if (
            status.full_text.find("software")     != -1 or 
            status.full_text.find(" tech ")       != -1 or 
            status.full_text.find(" tech.")       != -1 or 
            status.full_text.find("internet")     != -1 or 
            status.full_text.find("Internet")     != -1 or 
            status.full_text.find("computing")    != -1 or 
            status.full_text.find("Computing")    != -1 or 
            status.full_text.find("hacker")       != -1 or 
            status.full_text.find("hacking")      != -1 or 
            status.full_text.find("data")         != -1 or status.full_text.find("dados")         != -1 or
            status.full_text.find("Data")         != -1 or status.full_text.find("Dados")         != -1 or
            status.full_text.find("coding")       != -1 or status.full_text.find("codificar")     != -1 or
            status.full_text.find("programming")  != -1 or status.full_text.find("programação")   != -1 or
            status.full_text.find(" IT ")         != -1 or status.full_text.find(" TI ")          != -1 or 
            status.full_text.find("computation")  != -1 or status.full_text.find("computação")    != -1 or
            status.full_text.find("Computation")  != -1 or status.full_text.find("Computação")    != -1 or
            status.full_text.find("social media") != -1 or status.full_text.find("redes sociais") != -1 or
            status.full_text.find("Social media") != -1 or status.full_text.find("Redes sociais") != -1 or
            status.full_text.find("algorithm")    != -1 or status.full_text.find("algoritmo")     != -1 or
            status.full_text.find("Algorithm")    != -1 or status.full_text.find("Algoritmo")     != -1 or
            status.full_text.find("technology")   != -1 or status.full_text.find("tecnologia")    != -1 or
            status.full_text.find("Technology")   != -1 or status.full_text.find("Tecnologia")    != -1 or
            status.full_text.find("cloud")        != -1 or status.full_text.find("nuvem")         != -1 or
            status.full_text.find(" AI ")         != -1 or status.full_text.find(" IA ")          != -1 or
            status.full_text.find(" AI.")         != -1 or status.full_text.find(" IA.")          != -1 or
            status.full_text.find("artificial inteligence")   != -1 or status.full_text.find("inteligência artificial")  != -1 or
            status.full_text.find("Artificial Inteligence")   != -1 or status.full_text.find("Inteligência Artificial")  != -1 or
            status.full_text.find("requirements engineering") != -1 or status.full_text.find("engenharia de requisitos") != -1
            ):
            pass
        else:
            return

        print('---\nUsername: ' + status.user.screen_name)
        print(status.full_text)

        translated_tweet = GoogleTranslator(source='auto', target='pt').translate(status.full_text)
        
        translated_tweet = translated_tweet.replace("&amp;", "&")

        if(translated_tweet == status.full_text):
            # Updating last retweeted tweet
            self.last_tweet = status.full_text

            if not status.retweeted:
                # Retweet, since we have not retweeted it yet
                try:
                    self.api.retweet(status.id_str)
                    # self.api.update_status(translated_tweet, attachment_url='https://twitter.com/'+status.user.screen_name+'/status/'+status.id_str)
                except Exception as e:
                    # logger.error("Error on fav and retweet", exc_info=True)
                    return

        else:
            # Updating last retweeted tweet
            self.last_tweet = translated_tweet

            if not status.retweeted:
                # Retweet, since we have not retweeted it yet
                try:
                    # self.api.retweet(status.id)
                    self.api.update_status(translated_tweet, attachment_url='https://twitter.com/'+status.user.screen_name+'/status/'+status.id_str)
                except Exception as e:
                    try:
                        translated_tweet = GoogleTranslator(source='auto', target='pt').translate(st.text)
                        translated_tweet = translated_tweet.replace("&amp;", "&")
                        self.api.update_status(translated_tweet, attachment_url='https://twitter.com/'+st.user.screen_name+'/status/'+st.id_str)
                    except:
                        self.api.retweet(status.id_str)
                        # logger.error("Error on fav and retweet", exc_info=True)

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
    listen(string_list = ["ethics", "ethical", "ethically", "ética", "ético", "#ethicsBot", "#botEtico"])
