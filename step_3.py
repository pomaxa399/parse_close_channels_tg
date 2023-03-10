import json
import re
import csv
from tqdm import tqdm


def fix_content(file):
    
            
        with open(file, 'r', encoding='utf-8') as f:

            data = json.load(f)

            for item in data:
                content = item['content']

                if content is not None:
                    content = re.sub(r'<[^>]+>', '', content)
                    content = content.replace('\n', ' ').strip()
                    content = re.sub(r"[^\w\s]+", "", content)
                    content = ' '.join(content.split())
                    item['content'] = content

        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

with open('output.json', 'r', encoding='utf-8') as f:
    output_list = json.load(f)

# Удаление элементов, у которых image_url или video_preview равны None
output_list = [data for data in output_list if (data['image_url'] is not None or data['video_preview'] is not None) or data['content'] is not None]

# Сохранение изменений в файл
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(output_list, f, ensure_ascii=False, indent=4)

with open('data1.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['title', 'chat_id_or_url','post_id', 'date', 'content', 'image_url', 'video_preview', 'views'])
    for row in tqdm(output_list, desc='Записываем данные в файл data.csv'):
        writer.writerow([row['title'], row['chat_id_or_url'], row['post_id'], row['date'],
                        row['content'], row['image_url'], row['video_preview'], row['views']])


if __name__=='__main__':
    fix_content('output.json')