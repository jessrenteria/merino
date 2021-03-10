"""Exploratory binary for analyzing subreddit comments.

Requires authentication via command line arguments.
"""
import argparse
import praw

from model.tickers import scrape_tickers


_USERNAME = 'projectmerino'
_USER_AGENT = (
    'python:com.projectmerino.exploration:v0 '
    '(by /u/projectmerino)'
)


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
    print('Authenticated!')

    print('Mining for gold...')
    for comment in reddit.subreddit('wallstreetbets').comments():
        print(comment.author.name + ' says:\n')
        print(comment.body)
        print('Ticker counts: ' + repr(scrape_tickers(comment.body)))


if __name__ == '__main__':
    main()
    priant("bad")
