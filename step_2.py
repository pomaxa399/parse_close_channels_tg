import json
import os
from tqdm import tqdm
output_data = {}

def get_subfolders(path):
    subfolders = []
    for root, dirs, files in os.walk(path):
        for d in dirs:
            subfolders.append(os.path.join(root, d))
    return subfolders

# Список всех папок, начинающихся с "-"
folders = [f for f in os.listdir() if os.path.isdir(f) and f.startswith("-")]

# Список подпапок в каждой из папок
subfolders = []
for folder in folders:
    subfolders.extend(get_subfolders(folder))

with open('chat.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

output_list = []
for i in tqdm(data, desc="Сопоставляем файлы с постами"):
    
    output_data = {
        "title": i["sender_chat"]["title"],
        'chat_id_or_url': i['chat']['id'],
        'post_id': i['id'],
        "date": i['date'],
        "content": i.get('text') or i.get('caption') or i.get('poll', {}).get('text', ""),
        'image_url': None,
        "video_preview": None,
        "views": i.get('views', 0)
    }
    media_group_id = i.get('media_group_id')
    chat_id = i.get('chat').get('id')
    post_id = i.get('id')
    caption = i.get('caption')

    if chat_id:
        if media_group_id:
            # ваш код для обработки медиафайлов
            for mgs in subfolders:
            # Получаем список файлов в папке
                files = os.listdir(mgs)
                # for file in files:
                # Получаем полный путь к файлу
                file_path = os.path.join(mgs, ', '.join(files))
                # print(file_path)
                # Разбиваем путь на составляющие
                path_parts = file_path.split(os.sep)
                if path_parts[1] == str(media_group_id):
                    if caption:
                        output_data['image_url'] = file_path
                        break
        else:
            for mgs in subfolders:
            # Получаем список файлов в папке
                files = os.listdir(mgs)
                file_path = os.path.join(mgs, ', '.join(files))
                # Разбиваем путь на составляющие
                path_parts = file_path.split(os.sep)
                if path_parts[1] == str(post_id):
                    if os.path.basename(mgs) in ['photo', 'photo_wp']:
                        output_data['image_url'] = file_path
                        break
                    if os.path.basename(mgs) in ['video_prev']:
                        output_data['video_preview'] = file_path
                        break

    output_list.append(output_data)

# запись данных в новый JSON файл
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(output_list, f, ensure_ascii=False, indent=4)

