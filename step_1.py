import time
import json
import os
import shutil
from pyrogram import Client
from pyrogram.enums import ChatType, MessageMediaType
from pyrogram.errors import FloodWait
from tqdm import tqdm

api_id = 26665190  # Введите ваш API ID, полученный на сайте Telegram
api_hash = 'a5e6c4807949def45175d3e5bae75033'  # Введите ваш API Hash, полученный на сайте Telegram

limit = 100
chats = []
chats_id = []
texts = []
# Создаем клиент Telegram
with Client('my_account', api_id, api_hash) as client:
    try:
        dialogs = client.get_dialogs()

        for dial in tqdm(dialogs, desc='Собираем все посты'):
            if dial.chat.type in [ChatType.CHANNEL, ChatType.PRIVATE]:
                chats.append(dial)
    except FloodWait as e:
        time.sleep(e.value)

    with open('chats.txt', 'w', encoding='utf-8') as f:
        for chat in chats:
            f.write(str(chat) + '\n')

    with open('chats.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # заменяем }{ на },{
    json_data = ''.join(lines)
    json_data = json_data.replace('\n', '').replace('        ', '').replace('}{', '},{')

    # добавляем [ в начало и ] в конец
    json_data = '[' + json_data[:-1] + '}]'
    data = json.loads(json_data)

    # записываем в файл
    with open('chats.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    with open('chats.json', 'r', encoding='utf-8') as f:
        dialogs = json.load(f)

    for dialog in dialogs:
        chat_id = dialog['chat']['id']
        if str(chat_id).startswith('-'):
            chats_id.append(int(chat_id))

    try:
        for chat_id in tqdm(chats_id, desc='Скачиваем фото'):
            messages = client.get_chat_history(chat_id, limit=limit)
            for message in messages:
                texts.append(message)
                if message.media:

                    chat_folder = str(message.chat.id)

                    if message.media == MessageMediaType.PHOTO:

                        if message.media_group_id:
                            media_group_folder = str(message.media_group_id)
                            
                            filename = os.path.join(chat_folder, media_group_folder)
                        else:
                            filename = os.path.join(chat_folder, f'{message.id}\photo')
                        if not os.path.exists(filename):
                                os.makedirs(filename)
                       
                        img = client.download_media(message.photo.file_id)

                    elif message.media == MessageMediaType.WEB_PAGE:
                        filename = os.path.join(chat_folder, f'{message.id}\photo_wp')
                        if not os.path.exists(filename):
                            os.makedirs(filename)
                            img = client.download_media(message.web_page.photo.file_id)

                    elif message.media == MessageMediaType.VIDEO:
                        filename = os.path.join(chat_folder, f'{message.id}\\video_prev')
                        if not os.path.exists(filename):
                            os.makedirs(filename)
                        if message.video.thumbs is not None:
                            for thumb in message.video.thumbs:
                                img = client.download_media(thumb.file_id)
                                

                    shutil.copy(img, filename)

    except FloodWait as e:
        time.sleep(e.value)

with open('chat.txt', 'w', encoding='utf-8') as f:
    for msg in texts:
        f.write(str(msg) + '\n')

with open('chat.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# заменяем }{ на },{
json_data = ''.join(lines)
json_data = json_data.replace('\n', '').replace('        ', '').replace('}{', '},{')

# добавляем [ в начало и ] в конец
json_data = '[' + json_data[:-1] + '}]'
data = json.loads(json_data)

# записываем в файл
with open('chat.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
