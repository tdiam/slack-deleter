import argparse
import os
import time

import slack

from env import env_str


parser = argparse.ArgumentParser(
    description='Delete messages from slack between the given timestamps.\n'
                'Some replies may not be deleted since the from limit is '
                'based on the parent timestamps.'
)
parser.add_argument('channel', help='Channel ID')
parser.add_argument('--from_ts', help='First timestamp to delete', default='0000000000.000000')
parser.add_argument('--until_ts', help='Last timestamp to delete', default='9999999999.999999')


if __name__ == "__main__":
    args = parser.parse_args()
    client = slack.WebClient(token=env_str('SLACK_TOKEN'))
    response = client.conversations_history(channel=args.channel, limit=1000)
    matches = [
        msg for msg in response.data['messages'] if args.from_ts <= msg['ts'] <= args.until_ts
    ]

    deleted_count = 0
    for match in matches:
        for reply in match.get('replies', []):
            if reply['ts'] <= args.until_ts:
                client.chat_delete(channel=args.channel, ts=reply['ts'])
                time.sleep(1)
                deleted_count += 1
        client.chat_delete(channel=args.channel, ts=match['ts'])
        time.sleep(1)
        deleted_count += 1

    print(f'Successfully deleted {deleted_count} messages')
