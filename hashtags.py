import random

ht1 = [
    '#books', '#bookstagram', '#book', '#booklover', '#reading', '#bookworm', '#bookstagrammer', '#bookish', '#read', 
    '#booknerd', '#bookaddict', '#bibliophile', '#booksofinstagram', '#instabook', '#bookaholic',
    '#bookshelf', '#booksbooksbooks', '#libros', '#readersofinstagram', '#bookphotography',
    '#booklove',  '#art', '#literature', '#author' 
]

ht2 = [
    '#quotestagram', '#quotes', '#quoteoftheday', '#quotestoliveby', '#quote', '#inspirationalquotes', '#love',
    '#motivationalquotes', '#poetry', '#motivation', '#life', '#inspiration', '#quotesdaily', '#loveyourself', 
    '#positivevibes','#happy', '#success', '#quotesaboutlife', '#believe', '#selflove',
    '#happiness', '#thoughts', '#lifequotes'
]


def get_random_hashtags():
    ht = random.sample(ht1, 3) + random.sample(ht2, 3)
    # print(ht)
    return ht