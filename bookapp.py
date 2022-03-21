import sheets
from random import randint, choice
import time
from config import create_api
import tweepy
from hashtags import get_random_hashtags
from datetime import datetime, timedelta
import schedule
import threading

api = create_api()

HIGHLIGHT = 0
TITLE = 1
AUTHOR = 2


def tweet_now(msg):
    try:
        print(msg)
        return api.update_status(msg)
    except Exception as e:
        print(e)


def tweet_thread_now(msg, originaltweet):
    try:
        print(msg)
        return api.update_status(status=msg, in_reply_to_status_id=originaltweet.id, auto_populate_reply_metadata=True)
    except Exception as e:
        print(e)


def generate_tweet():
    row = sheets.get_random_highlight()
    # htags = get_random_hashtags()
    hl = row[HIGHLIGHT]
    attrib = f'\n-- from {row[TITLE]} by {row[AUTHOR]} '
    tweet = ''

    if len(hl) <= 280:
        if len(hl + attrib) <= 280:
            tweet = hl + attrib
            tweet_now(tweet[0:280])
        else:
            tweet = '1/2 '+hl
            originaltweet = tweet_now(tweet[0:280])
            tweet2 = '2/2 ' + attrib
            tweet_thread_now(tweet2[0:280], originaltweet)
    else:
        hl1 = '1/2 ' + hl[0:275]
        originaltweet = tweet_now(hl1)
        hl2 = '2/2 ' + hl[275:] + attrib
        tweet_thread_now(hl2[0:280], originaltweet)


def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()


print(f'script started successfully at: {datetime.now()}')
schedule.every(1).days.at("11:11").do(run_threaded, generate_tweet)
while True:
    schedule.run_pending()
    time.sleep(1)
