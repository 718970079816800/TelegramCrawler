#Search group links in Telegram messages.

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterEmpty
from telethon.errors.rpcerrorlist import ChannelPrivateError
import re

LINK1 = re.compile('https://t.me/(?P<link>[A-Za-z0-9_]+)')
LINK2 = re.compile('https://t.me/joinchat/(?P<link>[A-Za-z0-9_-]{22})')
CHANNELID = re.compile('channel_id=(?P<channelid>\d+)')
PEERS = []
Q = 'https://t.me/'
RESULTS = []
GROUPLINKS = []

api_id = XXX
api_hash = 'XXX'
phone = '+XXX'
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

def get_peer():
    'Get all your Telegram chat groups'
    global PEERS
    dialogs = client.iter_dialogs()
    for dialog in dialogs:
        if CHANNELID.findall(str(dialog.message)):
            PEERS.append(CHANNELID.search(str(dialog.message)).group('channelid'))
    PEERS = list(set(PEERS))
    PEERS.sort()

def search(q, peers):
    'Search group messages using the key word Q'
    global RESULTS
    global Q
    for peer in peers:
        try:
            result = client(SearchRequest(
                peer = int(peer),      # On which chat/conversation
                q = Q,      # What to search for
                filter = InputMessagesFilterEmpty(),  # Filter to use (maybe filter for media)
                min_date = None,  # Minimum date
                max_date = None,  # Maximum date
                offset_id = 0,    # ID of the message to use as offset
                add_offset = 0,   # Additional offset
                limit = 10,       # How many results
                max_id = 0,       # Maximum message ID
                min_id = 0,       # Minimum message ID
                hash = 0,
                from_id = None    # Who must have sent the message (peer)
            ))
            RESULTS.append(result)
        except ValueError as e:
            print(e)
        except ChannelPrivateError as e:
            print('Channel: {}'.format(int(peer)))
            print(e)
        
get_peer()
search(Q, PEERS)

for result in RESULTS:
    'Extract the group links from the searching result'
    if LINK1.findall(result.stringify()):
        GROUPLINKS.append('https://t.me/' + LINK1.search(result.stringify()).group('link'))
    if LINK2.findall(result.stringify()):
        GROUPLINKS.append('https://t.me/' + LINK2.search(result.stringify()).group('link'))

GROUPLINKS = list(set(GROUPLINKS))

for grouplink in GROUPLINKS:
    with open('grouplinks', 'a') as f:
        f.write(grouplink)
        f.write('\n')

