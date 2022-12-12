import json
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
import tweepy
import os

class EthicsListener(tweepy.StreamingClient):

    def __init__(self, bearer_token, api):
        self.last_tweet = "null"
        self.api = api

        return super(EthicsListener, self).__init__(bearer_token, wait_on_rate_limit=True)

    def on_data(self, raw_data):    
        data = json.loads(raw_data)

        try:
            id = data["data"]["id"]
            tweet = data["data"]["text"]
            text = tweet
        except:
            return
        
        ## Filters ##

        # Non Desired Terms
        if(
            text.find("$")                != -1 or
            text.find("100%")             != -1 or
            text.find("deal")             != -1 or
            text.find("Deal")             != -1 or
            text.find("buy")              != -1 or
            text.find("Buy")              != -1 or
            text.find("promotion")        != -1 or
            text.find("Promotion")        != -1 or
            text.find("purchase")         != -1 or
            text.find("Purchase")         != -1 or
            text.find("hacking")          != -1 or
            text.find("Hacking")          != -1 or
            text.find("hacker")           != -1 or
            text.find("Hacker")           != -1 or
            text.find("download")         != -1 or
            text.find("Download")         != -1 or
            text.find("product")          != -1 or
            text.find("Product")          != -1 or
            text.find("sale")             != -1 or
            text.find("Sale")             != -1 or
            text.find("market")           != -1 or
            text.find("Market")           != -1 or
            text.find("client")           != -1 or
            text.find("Client")           != -1 or
            text.find("costumer")         != -1 or
            text.find("Costumer")         != -1 or
            text.find("homework")         != -1 or
            text.find("Homework")         != -1 or
            text.find("assignment")       != -1 or
            text.find("Assignment")       != -1 or
            text.find("assignments")      != -1 or
            text.find("Assignments")      != -1 or
            text.find("pray")             != -1 or
            text.find("Pray")             != -1 or
            text.find("pay")              != -1 or
            text.find("Pay")              != -1 or
            text.find("RT")               != -1 or
            text.find("🔹")               != -1 or
            text.find("نمشے")             != -1 or
            text.find("#TransparencyARC") != -1 or
            text.find("#100DaysOfCode")   != -1 or
            text.find("#coding")          != -1 or
            text.find("#soulecting")      != -1 or
            #user == ("mediaethicsbot")   or # Reason: profile that post random content
            text == self.last_tweet
        ):
            return
        
        # Translating and correcting tweet
        translated_tweet = GoogleTranslator(source='auto', target='pt').translate(text[:4900])

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
            translated_tweet.find("tecno")         != -1 or
            translated_tweet.find("Tecno")         != -1 or
            translated_tweet.find(" AI ")          != -1 or
            #translated_tweet.find("#AIEthics")     != -1 or
            #translated_tweet.find("#AIethics")     != -1 or
            #translated_tweet.find("#aiethics")     != -1 or
            translated_tweet.find("inteligência artificial")  != -1 or
            translated_tweet.find("Inteligência Artificial")  != -1 or
            translated_tweet.find("engenharia de requisitos") != -1 or
            translated_tweet.find("Engenharia de requisitos") != -1 or
            translated_tweet.find("Engenharia de Requisitos") != -1 or
            text.find("data ethics")              != -1 or
            text.find("Data ethics")              != -1 or
            text.find("Data Ethics")              != -1 or 
            #text.find("#dataethics")              != -1 or 
            #text.find("#DataEthics")              != -1 or 
            text.find("internet ethics")          != -1 or
            text.find("Internet ethics")          != -1 or
            text.find("Internet Ethics")          != -1 or 
            text.find("social media ethics")      != -1 or
            text.find("Social media ethics")      != -1 or
            text.find("Social Media ethics")      != -1 or
            text.find("social media Ethics")      != -1 or
            text.find("Social media Ethics")      != -1 or
            text.find("Social Media Ethics")      != -1
            ):
            pass
        else:
            return

        if(translated_tweet == text):
            try:
                self.api.retweet(id)
            except Exception as e:
                return

        else:
            try:
                self.api.update_status(translated_tweet, attachment_url='https://twitter.com/user/status/'+id)
            except Exception as e:
                try:
                    self.api.update_status(translated_tweet[:275]+"...", attachment_url='https://twitter.com/user/status/'+id)
                except:
                    self.api.retweet(id)

        # Updating last retweeted tweet
        self.last_tweet = translated_tweet

    def on_errors(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            print(status_code)
            return False

def listen():
    
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

    bearer_token = str(os.environ.get('BEARER_TOKEN'))

    ethics_listener = EthicsListener(bearer_token, api)

    rule = tweepy.StreamRule(value = "(ethics OR ethical OR ethically OR ética OR ético OR #ethicsBot OR #botEtico) " + 
                                    "tweets_count:50 following_count:50 followers_count:50 -is:retweet -is:quote -is:reply -from:mediaethicsbot -from:ethicsBot_", tag='ethics')

    ethics_listener.add_rules(rule) # Define which strings to watch
    print(ethics_listener.get_rules())

    ethics_listener.filter() # Start the stream


if __name__ == "__main__":
    listen()
