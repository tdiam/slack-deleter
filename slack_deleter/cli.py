#!/usr/bin/env python

import argparse
import sys

from .delete_batch import BatchDeleter
from .delete_between import BetweenDeleter


class SlackDeleterCli:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Delete messages from Slack.',
            usage='''slack-delete <command> [<args>]

Available commands:
    batch   Delete messages from a list of timestamp IDs.
    between Delete messages between timestamps.
''')
        self.parser.add_argument('command', help='Subcommand to run')

    def cli(self):
        args = self.parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Invalid command', file=sys.stderr)
            self.parser.print_help()
            exit(1)
        getattr(self, args.command)(f'{self.parser.prog} {args.command}')

    def batch(self, prog):
        BatchDeleter().cli(sys.argv[2:], prog=prog)

    def between(self, prog):
        BetweenDeleter().cli(sys.argv[2:], prog=prog)


def main():
    SlackDeleterCli().cli()

if __name__ == '__main__':
    main()

