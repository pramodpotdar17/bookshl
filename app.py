import tweepy
import sheets
from random import randint
import time

consumer_key = 't1'
consumer_secret = 't2'
key = 't3-t4'
secret = '53'

HIGHLIGHT = 0
TITLE = 1
AUTHOR = 2
hashtags = '\n#highlights #books #quotes #daily'

def tweet_now(msg):
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(key, secret)
        api = tweepy.API(auth)
        try:
            api.verify_credentials()
            # print("Authentication OK")
        except:
            print("Error during authentication")
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        api.update_status(msg)
        # print(msg)
    except Exception as e:
        print(e)

def generate_tweet():
    row = sheets.get_random_highlight()
    hl = row[HIGHLIGHT]
    attrib = f'\n- from {row[TITLE]} by {row[AUTHOR]}\n'
    tweet = ''


    if len(hl) <= 280:
        if len(hl + attrib) <= 280:
            tweet = hl + attrib + hashtags
            tweet_now(tweet[0:280])
        else:
            tweet = hl + ' 1/2'
            tweet_now(tweet)
            tweet2 = attrib + '\n2/2\n' + hashtags
            tweet_now(tweet2[0:280])
    else:
        hl1 = hl[0:275] + ' 1/2'
        tweet_now(hl1)
        hl2 = hl[275:] + attrib + '\n2/2\n' + hashtags
        tweet_now(hl2)


def tweet_after_intervals():
    hour = randint(10,14)
    seconds = hour * 60 * 60
    while True:
        generate_tweet()
        print(f'sleeping...for....{hour} hours....')
        time.sleep(seconds)

tweet_after_intervals()


