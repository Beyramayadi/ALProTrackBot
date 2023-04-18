import tweepy
import apikeys
from datetime import date

# import all twitter keys/secrets

api_key = apikeys.api_key
api_key_secret = apikeys.api_key_secret
access_token = apikeys.access_token
access_token_secret = apikeys.access_token_secret
bearer_token = apikeys.bearer_token

client = tweepy.Client(bearer_token, api_key, api_key_secret,
                       access_token, access_token_secret)
auth = tweepy.OAuthHandler(api_key, api_key_secret,
                           access_token, access_token_secret)
api = tweepy.API(auth)
today = date.today()

client.create_tweet(text="✅ Today's 2023-04-17 results ✅ \nThe player who earned the most LP is NGX klownz 🇯🇴 (@Klownz99) with 128 LP gained in 13 games played (9 wins and 4 losses).")
