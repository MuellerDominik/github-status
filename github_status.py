#!/usr/bin/env python3

from time import sleep

from pytz import timezone
from datetime import datetime

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# OAuth token (user scope required)
api_token = '<access token>'

# Time zone
time_zone = 'Europe/Zurich'
_tz = timezone(time_zone)

# GitHub GraphQL API v4
endpoint = 'https://api.github.com/graphql'

# Transport
_transport = RequestsHTTPTransport(
    url=endpoint,
    use_json=True,
    headers={'Authorization': f'bearer {api_token}'}
)

# Client
client = Client(
    transport=_transport
)

def curr_time():
    # Current time
    return datetime.now(tz=_tz)

def time_suffix(now):
    # Emojis require 1-12 and not 0-11
    tf = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    # Suffix for 'clock' emoji
    time = f'{tf[now.hour % 12]}'
    if now.minute >= 30:
        time = f'{time}30'

    return time

def update_status_emoji(time):
    # GraphQL query
    query = gql(f'''
    mutation ChangeStatusEmoji {{
      changeUserStatus(input: {{emoji: ":clock{time}:"}}) {{
        status {{
          emoji
        }}
      }}
    }}
    ''')

    # Execute query and return result
    return client.execute(query)

def main():
    while True:
        # Update the status emoji
        now = curr_time()
        ts = time_suffix(now)
        transaction = update_status_emoji(ts)

        # Transaction log
        with open('transaction.log', 'a') as f:
            f.write(str(now) + ': ' + str(transaction) + '\n')

        # Sleep until the next hour or half-hour
        now = curr_time()
        sleep_time = 30 - now.minute
        if now.minute >= 30:
            sleep_time += 30

        sleep(sleep_time * 60 - now.second)

if __name__ == '__main__':
    main()
