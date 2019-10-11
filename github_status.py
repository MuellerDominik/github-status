#!/usr/bin/env python3

from pytz import timezone
from datetime import datetime

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# OAuth Token (user scope required)
api_token = '<access token>'

# Timezone
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

# Current time
now = datetime.now(tz=_tz)

# Emojis require 1-12 and not 0-11
tf = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# Suffix for 'clock' emoji
time = f'{tf[now.hour % 12]}'
if now.minute >= 30:
    time = f'{time}30'

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

client.execute(query)

def main():
    pass

if __name__ == '__main__':
    main()
