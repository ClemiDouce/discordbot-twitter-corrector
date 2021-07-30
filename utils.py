import requests

async def get_tweet_info(tweet_link, header):
    tweet_id = get_tweet_id(tweet_link)
    link = f"https://api.twitter.com/2/tweets/{tweet_id}?expansions=attachments.media_keys&media.fields=url"
    data = requests.get(link, headers=header)
    return data.text

def get_tweet_id(tweet_url):
    return tweet_url.split('/')[-1].split('?')[0]