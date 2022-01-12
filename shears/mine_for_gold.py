"""Exploratory binary for analyzing subreddit comments.

Requires authentication via command line arguments.
"""
import argparse
import praw
import json
 
from datetime import datetime
"""from model.tickers import get_ticker_set
from model.tickers import scrape_tickers"""

_USERNAME = 'noahbram'
_USER_AGENT = (
    'python:com.projectmerino.exploration:v0 '
    '(by /u/projectmerino)'
)
_SUBREDDIT_NAME = 'wallstreetbets'

""" Note: If you are only analyzing public comments, entering a username and password is optional. """
def main():
    parser = argparse.ArgumentParser(description='Mine for gold.')
    parser.add_argument(
        '--client_id',
        type=str,
        help='Reddit client id.'
    )
    parser.add_argument(
        '--client_secret',
        type=str,
        help='Reddit client secret.'
    )
    parser.add_argument(
        '--password',
        type=str,
        help='Reddit password.'
    )
    args = parser.parse_args()

    print('Authenticating Reddit API connection...')
    
    reddit = praw.Reddit(
        client_id=args.client_id,
        client_secret=args.client_secret,
        username=_USERNAME,
        password=args.password,
        user_agent=_USER_AGENT,
    )

    print(f'Authenticated as reddit user {reddit.user.me()}')

    print('Mining for gold...')
    """whitelist = get_ticker_set()"""

    updated_json = {}
    updated_json[_SUBREDDIT_NAME] = []
    current_data = {}

    with open('comments.json') as current_comments: 
        try: 
            current_data = json.load(current_comments)
        except:
            pass

    new_and_old_comments = []
    
    if _SUBREDDIT_NAME in current_data:
        new_and_old_comments.extend(current_data[_SUBREDDIT_NAME])

    for comment in reddit.subreddit(_SUBREDDIT_NAME).comments():
        if comment.id in new_and_old_comments:
            continue
        new_and_old_comments.append({
            comment.id :{
                'Date': datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                'Name': comment.author.name, 
                'Body': comment.body, 
                'Votes': comment.score
            }})
    current_data[_SUBREDDIT_NAME] = new_and_old_comments
    updated_json[_SUBREDDIT_NAME] = current_data[_SUBREDDIT_NAME]

    with open('comments.json', 'w') as outfile:
        json.dump(updated_json, outfile, indent=4, sort_keys=True)


if __name__ == '__main__':
    main()
