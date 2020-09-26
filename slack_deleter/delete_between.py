import argparse
import os
import time

import slack

from .env import env_str


class BetweenDeleter:
    def cli(self, argv, prog=None):
        parser = argparse.ArgumentParser(
            prog=prog,
            description='Delete messages between the given timestamps.\n'
                'Some replies may not be deleted since the limits are '
                'based on the parent timestamps.'
        )
        parser.add_argument('channel', help='Channel ID')
        parser.add_argument('--from_ts', help='First timestamp to delete', default='0000000000.000000')
        parser.add_argument('--until_ts', help='Last timestamp to delete', default='9999999999.999999')

        args = parser.parse_args(argv)
        delete_count = self.run(args)
        if delete_count:
            print(f'Successfully deleted {delete_count} messages')
        else:
            print(f'No messages found')

    def run(self, args):
        client = slack.WebClient(token=env_str('SLACK_TOKEN'))
        response = client.conversations_history(channel=args.channel, limit=1000)
        matches = [
            msg for msg in response.data['messages'] if args.from_ts <= msg['ts'] <= args.until_ts
        ]

        delete_count = 0
        for match in matches:
            for reply in match.get('replies', []):
                if reply['ts'] <= args.until_ts:
                    client.chat_delete(channel=args.channel, ts=reply['ts'])
                    time.sleep(1)
                    delete_count += 1
            client.chat_delete(channel=args.channel, ts=match['ts'])
            time.sleep(1)
            delete_count += 1

        return delete_count

