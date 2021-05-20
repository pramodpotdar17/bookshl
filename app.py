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
        api.update_status(msg)
    except Exception as e:
        print(e)


def generate_tweet():
    row = sheets.get_random_highlight()
    htags = get_random_hashtags()
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
    friends = tweepy.Cursor(api.friends, screen_name).items(300)
    return [friend.screen_name for friend in friends]

def get_user_followers(screen_name):
    followers = tweepy.Cursor(api.followers, screen_name).items(300)
    return [follower.screen_name for follower in followers]

def unfollow_non_followers():
    userid = api.me().id
    followers = get_user_followers(userid)
    friends = get_user_friends(userid)
    # with open('friends.txt', 'w') as f:
    #     f.write(str(friends))
    #     f.close()
    # with open('followers.txt', 'w') as f:
    #     f.write(str(followers))
    #     f.close()

    non_followers = [f for f in friends if f not in followers]
    # with open('non_followers.txt', 'w') as f:
    #     f.write(str(non_followers))
    #     f.close()
    print(f'non follower len ---- {len(non_followers)}')

    for nf in non_followers:
        try:
            print(f'unfollowing this dush {nf}')
            api.destroy_friendship(nf)
            time.sleep(2)
        except Exception as e:
            print(f'could not unfollow dush {nf}')
            print(e)


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


def like_tweets():
    htags = get_random_hashtags()
    tweets = get_tweets_by_hashtags(choose_word(htags))
    count = 0
    # potential_follows = []
    for tweet in tweets:
        try:
            like_tweet(tweet)
            # potential_follows.append(tweet.user.screen_name)
            count += 1
        except Exception as e:
            print('exeption occrod while iterating..', e)

def follow_tweeters():
    htags = get_random_hashtags()
    tweets = get_tweets_by_hashtags(choose_word(htags))
    count = 0
    for tweet in tweets:
        try:
            follow_user(tweet.user.screen_name)
            count += 1
        except Exception as e:
            print('error while following', e)

def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()

schedule.every(1).days.at("08:01").do(run_threaded, generate_tweet)
schedule.every(1).days.at("23:01").do(run_threaded, generate_tweet)
schedule.every(1).days.at("16:31").do(run_threaded, generate_tweet)

schedule.every(1).days.at("09:11").do(run_threaded, like_tweets)
schedule.every(1).days.at("00:11").do(run_threaded, like_tweets)
schedule.every(1).days.at("17:11").do(run_threaded, like_tweets)


schedule.every(12).hours.do(run_threaded, follow_followers)
schedule.every(16).hours.do(run_threaded, follow_tweeters)


schedule.every(2).days.at("06:01").do(run_threaded, unfollow_non_followers)

while True:
    schedule.run_pending()
    time.sleep(1)
    