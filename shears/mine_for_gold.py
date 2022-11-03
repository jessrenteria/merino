"""Exploratory binary for analyzing subreddit comments.

Requires authentication via command line arguments.
"""
import argparse
import random
import socket
import sqlite3
import praw
from praw.models import MoreComments
import pandas as pd 

from model.tickers import get_ticker_set
from model.tickers import scrape_tickers

_USERNAME = 'noahbram'
_USER_AGENT = (
    'Comment Extraction '
    '(by u/{username})'.format(username = _USERNAME)
)
_SUB_REDDIT = 'wallstreetbets'

conn = sqlite3.connect('db.sqlite')

def getCommentsDataFrame(reddit, sudreddit):
    body = []
    name = []
    tickerCount = []
    for comment in reddit.subreddit(sudreddit).comments():
        if not isinstance(comment, MoreComments):
            body.append(comment.body)
            name.append(comment.author.name)
            tickerCount.append(repr(scrape_tickers(comment.body, whitelist=get_ticker_set())))
    comments_dict = {
        "Body" : body,
        "Name" : name,
        "Ticker Count" : tickerCount,
    }

    comments_df = pd.DataFrame(data=comments_dict)
    return(comments_df)

def check_if_valid_chart_data(df: pd.DataFrame) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print("No comments. Finishing execution")
        return False 

    # Primary Key Check
    # if pd.Series(df['Ticker Count']).is_unique:
    #     pass
    # else:
    #     raise Exception("Primary Key check is violated: At least one of the returned comments have the same Ticker")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found")

    return True

def validateCommentsDataFrame(reddit, subreddit):
    comments_df = pd.DataFrame(getCommentsDataFrame(reddit, subreddit), columns=["Name", "Ticker Count", "Body"])

    # Validate
    if check_if_valid_chart_data(comments_df):
        print("Data valid, proceed to Load stage")
    else: return pd.DataFrame()

    # Load
    print("Opened database successfully")

    try:
        comments_df.to_sql("{subreddit}_chart".format(subreddit = subreddit), conn, index=False, if_exists='replace')
    except:
        print("Data already exists in the database")
        return pd.DataFrame()
    
    df = pd.read_sql_query("SELECT * FROM {subreddit}_chart".format(subreddit = subreddit), conn, parse_dates=["date"])

    conn.commit()
    print("Close database successfully")
    return df


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
    # whitelist = get_ticker_set()
    # for comment in reddit.subreddit(_SUB_REDDIT).comments():
    #     print(comment.author.name + ' says:\n')
    #     print(comment.body)
    #     print('Ticker counts: ' + repr(scrape_tickers(comment.body, whitelist=whitelist)))

    # print(getCommentsDataFrame(reddit,_SUB_REDDIT, whitelist).head())
    comments_df = validateCommentsDataFrame(reddit, _SUB_REDDIT)
    print(comments_df.head())

if __name__ == '__main__':
    main()