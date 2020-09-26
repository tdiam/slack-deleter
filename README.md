# slack-deleter

CLI tools to bulk delete messages from Slack.

## Getting started

### Installation
1. ([Install Poetry](https://python-poetry.org/docs/#installation) if needed).
1. Clone this repository.
1. Run `poetry install`.
```bash
git clone https://github.com/tdiam/slack-deleter
cd slack-deleter
poetry install
```

### Create app
In order to use this tool in your Slack workspace, you need to create an "app".

1. [Create app](https://api.slack.com/apps?new_app=1).
1. From the "Add features and functionality" panel click on "Permissions".
1. Click on "Add an OAuth Scope" under "User Token Scopes".
1. Add the `channels:history` and `chat:write` permissions.
1. Click on "Install App to Workspace".
1. Hooray, you now have your "OAuth Access Token" (the one starting with `xoxp`)!

### Create .env
Copy the `env.sample` file to `.env` and replace the `SLACK_TOKEN` value with the OAuth Access Token you obtained.

## Usage
```bash
poetry shell
slack-delete <command> [<args>]
```

### Available commands
```bash
# As printed by `slack-delete --help`
usage: slack-delete <command> [<args>]

Available commands:
    batch   Delete messages from a list of timestamp IDs.
    between Delete messages between timestamps.
```

For detailed command syntax, run `slack-delete <command> --help`.

### Examples
#### Batch delete
```
slack-delete batch CUCF5C996 p1600870610000500 p1600920629000110 p1599182440024000 p1598788187006000 p1599679370045000
```

#### Delete between timestamps
```
slack-delete between CUCF5C996 --from_ts 1600870610.000000 --until_ts 1600920629.000000
```

#### Delete all from yesterday
```
slack-delete between CUCF5C996 --from_ts $(date --date='yesterday' +%s.000000)
```

