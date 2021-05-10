"""Exploratory binary for analyzing subreddit comments.

Requires authentication via command line arguments.
"""
import argparse
import praw
from requests import Session

from model.tickers import get_ticker_set
from model.tickers import scrape_tickers


_USERNAME = 'projectmerino'
_USER_AGENT = (
    'python:com.projectmerino.exploration:v0 '
    '(by /u/projectmerino)'
)

session = Session()
session.verify = "/path/to/certfile.pem" 

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
    
    """Authorized Reddit Instances"""
    reddit = praw.Reddit(
        client_id=args.client_id,
        client_secret=args.client_secret,
        username=_USERNAME,
        password=args.password,
        user_agent=_USER_AGENT,
    )
    print('Authenticated!')

    print('Mining for gold...')
    whitelist = get_ticker_set()

    updated_json = {}
    updated_json["wallstreetbets"] = []
    try:
        with open('comments.json') as current_comments:    
            current_data = json.load(current_comments)
            all_new_comments = []
            for dicObj in current_data["wallstreetbets"]:
                all_new_comments.append(dicObj)
            for comment in reddit.subreddit('wallstreetbets').comments():
                all_new_comments.append({"Name": comment.author.name, "Body": comment.body,})
            current_data["wallstreetbets"] = all_new_comments
            updated_json["wallstreetbets"] = current_data["wallstreetbets"]
            with open('comments.json', 'w') as outfile:
                json.dump(updated_json, outfile)
    except IOError as io:
        print( "ERROR: " + io)

if __name__ == '__main__':
    main()
