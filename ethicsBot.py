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
            status.full_text.find("$")                != -1 or
            status.full_text.find("100%")             != -1 or
            status.full_text.find("deal")             != -1 or
            status.full_text.find("Deal")             != -1 or
            status.full_text.find("buy")              != -1 or
            status.full_text.find("Buy")              != -1 or
            status.full_text.find("promotion")        != -1 or
            status.full_text.find("Promotion")        != -1 or
            status.full_text.find("purchase")         != -1 or
            status.full_text.find("Purchase")         != -1 or
            status.full_text.find("hacking")          != -1 or
            status.full_text.find("Hacking")          != -1 or
            status.full_text.find("hacker")           != -1 or
            status.full_text.find("Hacker")           != -1 or
            status.full_text.find("download")         != -1 or
            status.full_text.find("Download")         != -1 or
            status.full_text.find("product")          != -1 or
            status.full_text.find("Product")          != -1 or
            status.full_text.find("sale")             != -1 or
            status.full_text.find("Sale")             != -1 or
            status.full_text.find("market")           != -1 or
            status.full_text.find("Market")           != -1 or
            status.full_text.find("client")           != -1 or
            status.full_text.find("Client")           != -1 or
            status.full_text.find("costumer")         != -1 or
            status.full_text.find("Costumer")         != -1 or
            status.full_text.find("homework")         != -1 or
            status.full_text.find("Homework")         != -1 or
            status.full_text.find("assignment")       != -1 or
            status.full_text.find("Assignment")       != -1 or
            status.full_text.find("assignments")      != -1 or
            status.full_text.find("Assignments")      != -1 or
            status.full_text.find("pay")              != -1 or
            status.full_text.find("Pay")              != -1 or
            status.full_text.find("RT")               != -1 or
            status.full_text.find("🔹")               != -1 or
            status.full_text.find("نمشے")             != -1 or
            status.full_text.find("#TransparencyARC") != -1 or
            status.full_text.find("#100DaysOfCode")   != -1 or
            status.full_text.find("#coding")          != -1 or
            status.full_text.find("#soulecting")      != -1 or
            status.user.screen_name == ("mediaethicsbot")   or # Reason: profile that post random content
            status.full_text == self.last_tweet
        ):
            return
        
        # Translating and correcting tweet
        translated_tweet = GoogleTranslator(source='auto', target='pt').translate(status.full_text)

        translated_tweet = translated_tweet.replace("&amp;", "&")
        translated_tweet = translated_tweet.replace("&lt;", "<")
        translated_tweet = translated_tweet.replace("&gt;", ">")
        translated_tweet = translated_tweet.replace("&gt;&gt;", ">>")

        # Non Desired Terms
        if(
            translated_tweet.find("comissão de ética") != -1 or
            translated_tweet.find("Comissão de Ética") != -1 or
            translated_tweet.find("vaga")              != -1 or
            translated_tweet.find("Vaga")              != -1 or
            translated_tweet.find("contrate")          != -1 or
            translated_tweet.find("Contrate")          != -1 or
            translated_tweet.find("contratar")         != -1 or
            translated_tweet.find("Contratar")         != -1 or
            translated_tweet.find("curso pago")        != -1 or
            translated_tweet.find("Curso pago")        != -1 or
            translated_tweet.find("whatsapp")          != -1 or
            translated_tweet.find("Whatsapp")          != -1
        ):
            return

        # Related Terms
        if (
            translated_tweet.find("ciber")         != -1 or 
            translated_tweet.find("Ciber")         != -1 or 
            translated_tweet.find("ética virtual") != -1 or 
            translated_tweet.find("Ética virtual") != -1 or 
            translated_tweet.find("Ética Virtual") != -1 or 
            translated_tweet.find("ética digital") != -1 or 
            translated_tweet.find("Ética digital") != -1 or 
            translated_tweet.find("Ética Digital") != -1 or 
            translated_tweet.find("software")      != -1 or 
            translated_tweet.find("Software")      != -1 or
            translated_tweet.find("codificar")     != -1 or 
            translated_tweet.find("Codificar")     != -1 or 
            translated_tweet.find("programação")   != -1 or
            translated_tweet.find("Programação")   != -1 or
            translated_tweet.find("computação")    != -1 or
            translated_tweet.find("Computação")    != -1 or
            translated_tweet.find("algoritmo")     != -1 or
            translated_tweet.find("Algoritmo")     != -1 or
            # translated_tweet.find("tecno")         != -1 or
            # translated_tweet.find("Tecno")         != -1 or
            translated_tweet.find(" AI ")          != -1 or
            # translated_tweet.find("#AIEthics")     != -1 or
            # translated_tweet.find("#AIethics")     != -1 or
            # translated_tweet.find("#aiethics")     != -1 or
            translated_tweet.find("inteligência artificial")  != -1 or
            translated_tweet.find("Inteligência Artificial")  != -1 or
            translated_tweet.find("engenharia de requisitos") != -1 or
            translated_tweet.find("Engenharia de requisitos") != -1 or
            translated_tweet.find("Engenharia de Requisitos") != -1 or
            status.full_text.find("data ethics")              != -1 or
            status.full_text.find("Data ethics")              != -1 or
            status.full_text.find("Data Ethics")              != -1 or 
            # status.full_text.find("#dataethics")              != -1 or 
            # status.full_text.find("#DataEthics")              != -1 or 
            status.full_text.find("internet ethics")          != -1 or
            status.full_text.find("Internet ethics")          != -1 or
            status.full_text.find("Internet Ethics")          != -1 or 
            status.full_text.find("social media ethics")      != -1 or
            status.full_text.find("Social media ethics")      != -1 or
            status.full_text.find("Social Media ethics")      != -1 or
            status.full_text.find("social media Ethics")      != -1 or
            status.full_text.find("Social media Ethics")      != -1 or
            status.full_text.find("Social Media Ethics")      != -1
            ):
            pass
        else:
            return
        
        # Finding last url to remove when saving last tweet
        try:
            url = status.entities['urls'][0].get('url')
        except:
            url = ""

        if(translated_tweet == status.full_text):
            if not status.retweeted:
                # Retweet, since we have not retweeted it yet
                try:
                    self.api.retweet(status.id_str)
                except Exception as e:
                    return

        else:
            # If a similar tweet was just published, return
            if(self.last_tweet == translated_tweet.replace(url, "")): return

            # Updating last retweeted tweet
            self.last_tweet = translated_tweet.replace(url, "")

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
