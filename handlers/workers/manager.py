from asyncio import sleep
from pprint import pprint
import sqlite3

import requests
import vk_api
from data.config import VK_TOKEN, PATH_TO_DB
from loader import dp



token = VK_TOKEN

class AdminDB:
    def __init__(self):
        conn = sqlite3.connect(PATH_TO_DB)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
                          id INTEGER PRIMARY KEY,
                          text TEXT NOT NULL,
                          photo TEXT,        
                          publish INTEGER,
                          video TEXT
                       )''')
        conn.commit()
        conn.close()

    async def add_row(self, id, text, photo, pub=0, video=""):
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT or IGNORE INTO posts (id, text, photo, publish, video) VALUES (?, ?, ?, ?, ?)", (id, text, photo, pub, video))
            cursor.close()

    async def get_post_not_publish(self):
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()
            query = cursor.execute("SELECT * FROM posts WHERE publish=0")
            return query.fetchall()

    async def get_post_for_id(self,id):
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()
            query = cursor.execute("SELECT * FROM posts WHERE id=(?)",(id,))
            return query.fetchone()

    async def remove_post_publush(self):
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()
            try:
                # Выполняем SQL-запрос для удаления записи по ID
                cursor.execute("DELETE FROM posts WHERE publish=1",)
                conn.commit()
                print("Запись с ID", id, "была успешно удалена.")
            except sqlite3.Error as e:
                print("Ошибка при удалении записи:", e)

    async def publish_post(self, id):
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()
            cursor.execute(f'UPDATE posts SET publish = 1 WHERE id = (?)', (id,))
            conn.commit()

    async def delete_last_records_if_exceed_limit(self, delete_count=30):
        # Подключение к базе данных
        conn = sqlite3.connect(PATH_TO_DB)
        cursor = conn.cursor()

        try:
            # Проверяем общее количество записей в таблице
            cursor.execute(f"SELECT COUNT(*) FROM posts")
            total_records = cursor.fetchone()[0]

            if total_records > 100:
                # Получаем ID последних записей, которые нужно удалить
                cursor.execute(f"SELECT id FROM posts ORDER BY id DESC LIMIT {delete_count}")
                record_ids_to_delete = [row[0] for row in cursor.fetchall()]

                # Удаляем записи с найденными ID
                cursor.execute(f"DELETE FROM posts WHERE id IN ({','.join(map(str, record_ids_to_delete))}) AND publish=1")
                conn.commit()

                print(f"Удалено {len(record_ids_to_delete)} записей из таблицы posts.")
            else:
                print("Общее количество записей не превышает указанный лимит. Удаление не требуется.")

        except sqlite3.Error as e:
            print("Ошибка при выполнении SQL-запроса:", e)
        finally:
            # Закрываем соединение с базой данных
            conn.close()



async def get_all_well(GROUP_IDs):
    session = vk_api.VkApi(token=token)
    vk = session.get_api()
    keys_list = list(GROUP_IDs.keys())
    for group in keys_list:
        try:
            await sleep(12)
            wall_posts = vk.wall.get(owner_id=group,
                                     count=4, filter='owner', extended=1)  # Здесь count - количество получаемых записей (в данном примере 10)
            adb = AdminDB()
            for post in wall_posts["items"]:


                if post['attachments'] and 'text' in post:
                    photo_urls = []
                    for attachment in post['attachments']:
                        if attachment['type'] == 'photo':
                            photo_info = attachment['photo']
                            photo_url = max(photo_info['sizes'], key=lambda x: x['height'])['url']
                            photo_urls.append(photo_url)
                    if photo_urls:
                        photo_str = ""
                        if photo_urls:
                            photo_str = ",".join(photo_urls)
                        id = int(group) + post['id']
                        video_str = ''
                        post_text = post['text'] + "*//*" + GROUP_IDs[group] +'*//*' + group[1:]
                        await adb.add_row(id, post_text, photo_str, 0, video_str)
                        #except Exception as error:
                        #    print("Ошибка в методе get_all_well, при сожранение строки в базу данных:", error)
        except vk_api.VkApiError as e:
            print("API error:", e)



def get_diveo(url):
    with open("file_name.mp4", "wb") as file:
        file.write(url)


if __name__ == "__main__":
    f = AdminDB()
    get_diveo('https://vk.com/video-220310598_456239115')

