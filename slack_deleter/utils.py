import time

import slack

from .env import env_str


def get_client():
    token = env_str('SLACK_TOKEN')
    client = slack.WebClient(token=token)
    return client

def normalize_timestamp(ts):
    """
    Normalize Slack message timestamp.

    Removes 'p' prefix and adds decimal separator if needed.
    """
    ts = str(ts)
    if ts[0] == 'p':
        ts = ts[1:]
    if '.' not in ts:
        ts = ts[:-6] + '.' + ts[-6:]

    return ts

