import argparse
import os
import time

import slack

from .env import env_str


class BatchDeleter:
    def cli(self, argv, prog=None):
        parser = argparse.ArgumentParser(
            prog=prog,
            description='Delete messages from a list of timestamp IDs. Replies are also deleted.'
        )
        parser.add_argument('channel', help='Channel ID')
        parser.add_argument('ts', nargs='+', help='Timestamps of messages')

        args = parser.parse_args(argv)
        delete_count = self.run(args)
        if delete_count:
            print(f'Successfully deleted {delete_count} messages')
        else:
            print('No messages found')

    def run(self, args):
        client = slack.WebClient(token=env_str('SLACK_TOKEN'))
        response = client.conversations_history(channel=args.channel, limit=1000)
        matches = [
            msg for msg in response.data['messages'] if msg['ts'] in args.ts
        ]

        delete_count = 0
        for parent in matches:
            replies = parent.get('replies', [])

            for reply in replies:
                client.chat_delete(channel=args.channel, ts=reply['ts'])
                time.sleep(1)
                delete_count += 1
            client.chat_delete(channel=args.channel, ts=parent['ts'])
            time.sleep(1)
            delete_count += 1

        return delete_count

