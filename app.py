import sheets
from random import randint, choice
import time
from config import create_api
import tweepy
from hashtags import get_random_hashtags
from datetime import datetime, timedelta

api = create_api()

HIGHLIGHT = 0
TITLE = 1
AUTHOR = 2
htags = get_random_hashtags()

def tweet_now(msg):
    try:
        api.update_status(msg)
    except Exception as e:
        print(e)


def generate_tweet():
    row = sheets.get_random_highlight()
    hl = row[HIGHLIGHT]
    attrib = f'\n- from {row[TITLE]} by {row[AUTHOR]}\n'
    tweet = ''
    htag_str = ' '.join(htags)

    if len(hl) <= 280:
        if len(hl + attrib) <= 280:
            tweet = hl + attrib + htag_str
            tweet_now(tweet[0:280])
        else:
            tweet = hl + ' 1/2'
            tweet_now(tweet)
            tweet2 = attrib + '\n2/2\n' + htag_str
            tweet_now(tweet2[0:280])
    else:
        hl1 = hl[0:275] + ' 1/2'
        tweet_now(hl1)
        hl2 = hl[275:] + attrib + '\n2/2\n' + htag_str
        tweet_now(hl2[0:280])

# follow single user based on username / id
def follow_user(usercreds):
    try:
        api.create_friendship(usercreds)
        time.sleep(3)
    except Exception as e:
        print(e)

# like a single tweet
def like_tweet(tweet):
    try:
        if tweet.in_reply_to_status_id is not None or tweet.user.id == api.me().id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            tweet.favorite()
            time.sleep(2)
    except Exception as e:
        print("Error on like\n", e)

def get_user_friends(screen_name):
    friends = api.friends(screen_name)
    return [friend.screen_name for friend in friends]

def get_user_followers(screen_name):
    followers = api.followers(screen_name)
    return [follower.screen_name for follower in followers]

def get_tweets_by_hashtags(word):
    date = datetime.now() - timedelta(days=1)
    date_since = date.strftime('%Y-%m-%d')
    numtweet = 25
    tweets = tweepy.Cursor(api.search, q=word, lang="en",
                           since=date_since, tweet_mode='extended').items(numtweet)
    
    list_tweets = [tweet for tweet in tweets]
    return list_tweets


def follow_followers():
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            try:
                follower.follow()
                time.sleep(2)
            except tweepy.error.TweepError:
                print('error while following')

def choose_word(hashlist):
    return choice(hashlist).strip('#')

def start_bot():
    generate_tweet()
    time.sleep(3)
    tweets = get_tweets_by_hashtags(choose_word(htags))
    print(len(tweets))
    follow_followers()
    time.sleep(15 * 60)
    count = 0
    potential_follows = []
    for tweet in tweets:
        try:
            like_tweet(tweet)
            potential_follows.append(tweet.user.screen_name)
            count += 1
        except Exception as e:
            print('exeption occrod while iterating..', e)
    count = 0

    for screen_name in potential_follows:
        try:
            follow_user(screen_name)
            count += 1
            if count > 25: 
                break
            potential_follows += get_user_friends(tweet.user.screen_name)
        except Exception as e:
            print('error while following', e)


def tweet_after_intervals():
    hour = 8
    seconds = hour * 60 * 60
    while True:
        start_bot()
        print(f'sleeping...for....{hour} hours....')
        time.sleep(seconds)

tweet_after_intervals()