"""Exploratory binary for analyzing subreddit comments.

Requires authentication via command line arguments.
"""
import argparse
import praw

from model.nasdaq_screener import parse_nasdaq_screener
from model.tickers import scrape_tickers, Ticker


_USERNAME = 'projectmerino'
_USER_AGENT = (
    'python:com.projectmerino.exploration:v0 '
    '(by /u/projectmerino)'
)


def get_whitelist(filepaths: list[str]) -> frozenset[Ticker]:
    """Get whitelist from NASDAQ screener data."""
    tickers = set()
    for filepath in filepaths:
        for stock in parse_nasdaq_screener(filepath):
            tickers.add(stock.symbol)
    return frozenset(tickers)


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
    parser.add_argument(
        '--screener_csv',
        action='append',
        type=str,
        help='NASDAQ screener CSV filepath. May be specified multiple times.'
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
    whitelist = None
    if args.screener_csv:
        whitelist = get_whitelist(args.screener_csv)
    for comment in reddit.subreddit('wallstreetbets').comments():
        print(comment.author.name + ' says:\n')
        print(comment.body)
        print('Ticker counts: ' + repr(scrape_tickers(comment.body,
                                                      whitelist=whitelist)))


if __name__ == '__main__':
    main()
