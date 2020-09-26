import argparse
import os
import time

from .utils import get_client, normalize_timestamp


class BatchDeleter:
    def cli(self, argv, prog=None):
        parser = argparse.ArgumentParser(
            prog=prog,
            description='Delete messages from a list of timestamp IDs. Replies are also deleted.'
        )
        parser.add_argument('channel', help='Channel ID')
        parser.add_argument('ts', nargs='+', help='Timestamps of messages (format: 1586185432.000100 or 1586185432000100 or p1586185432000100)')

        args = parser.parse_args(argv)
        delete_count = self.run(args)
        if delete_count:
            print(f'Successfully deleted {delete_count} messages')
        else:
            print('No messages found')

    def run(self, args):
        client = get_client()
        response = client.conversations_history(channel=args.channel, limit=1000)
        ts = [normalize_timestamp(t) for t in args.ts]
        matches = [
            msg for msg in response.data['messages'] if msg['ts'] in ts
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

