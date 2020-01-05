#Get Telegram group members info
#phone number,username,user id,access hash,name,group name,group id,time
#Store as GroupId-GroupName.csv

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.sync import TelegramClient
import csv
import sys
import datetime
import os
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

api_id = XXXXX#Replace
api_hash = 'XXXXXXXXXXXXXXXXXXX'#Replace
phone = '+XXXXXXXXXXX'#Replace
client = TelegramClient(phone, api_id, api_hash)
day = datetime.date.today()

try:
    os.makedirs(str(day))
except FileExistsError:
    pass
try:
    os.chdir(os.getcwd()+'\\'+str(day))#If you work in Windows.
except FileNotFoundError:
    os.chdir(os.getcwd()+'/'+str(day))#if you work in Linux.

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

chats = []
last_date = None
chunk_size = 20000
groups = []

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
        ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        #groups.append(chat)
        continue

i=0

for g in groups:
    try:
        print(str(i) + '-' + str(g.id) + '-' + g.title)
    except UnicodeEncodeError as e:
        print(str(i) + '-' + str(g.id) + '-' + g.title.translate(non_bmp_map))
    i += 1
    print('Fetching Members...')
    all_participants = []
    all_participants = client.get_participants(g, aggressive=True)
    try:
        print(g.title + 'Saving')
    except UnicodeEncodeError as e:
        print(g.title.translate(non_bmp_map) + 'Saving')
    filename = str(g.id) + '-' + g.title.replace(r'*', '').replace(r'/', '').replace(r'\\', '').replace(r'>', '').replace(r'<', '').replace(r'"', '').replace(r':', '').replace(r'?', '').replace(r'|', '') + '.csv'
    with open(filename,"w",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['phone','username','user id','access hash','name','group', 'group id', 'time'])
        for user in all_participants:
            if user.username:
                username = user.username
            else:
                username = ""
            if user.first_name:
               first_name = user.first_name
            else:
                first_name = ""
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ""
            name= (first_name + ' ' + last_name).strip()
            if user.phone:
                phone = user.phone
            else:
                phone = ''
            writer.writerow([phone, username, user.id, user.access_hash, name, g.title, g.id, str(day)])      
    print('Members scraped successfully.')

client.disconnect()
