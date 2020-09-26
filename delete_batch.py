import argparse
import os
import time

import slack

from env import env_str


parser = argparse.ArgumentParser(
    description='Batch-delete messages from slack. Replies are also deleted.'
)
parser.add_argument('channel', help='Channel ID')
parser.add_argument('ts', nargs='+', help='Timestamps of messages')


if __name__ == "__main__":
    args = parser.parse_args()
    delete_count = 0
    client = slack.WebClient(token=env_str('SLACK_TOKEN'))
    response = client.conversations_history(channel=args.channel, limit=1000)
    matches = [
        msg for msg in response.data['messages'] if msg['ts'] in args.ts
    ]
    if not matches:
        print('Thread not found')
        exit()

    for parent in matches:
        replies = parent.get('replies', [])

        for reply in replies:
            client.chat_delete(channel=args.channel, ts=reply['ts'])
            time.sleep(1)
            delete_count += 1
        client.chat_delete(channel=args.channel, ts=parent['ts'])
        time.sleep(1)
        delete_count += 1

    print(f'Successfully deleted {delete_count} messages')
