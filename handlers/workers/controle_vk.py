import sqlalchemy
import vk_api

from handlers.workers.control_db import DBAlchemy


class VK_Manager:
    def __init__(self, token):
        self.token = token
        session = vk_api.VkApi(token=self.token)
        self.vk = session.get_api()

    # забираем посты со стены count=4
    async def get_posts_info(self, group):
        try:
            wall_posts = self.vk.wall.get(owner_id=group,
                                     count=4, filter='owner',
                                     extended=1)
            return wall_posts['items']
        except vk_api.VkApiError as e:
            print("VkApiError - get_posts_info:", e)

    # добавляем посты в базу данных
    async def add_post(self, group_id:dict):
        groups = list(group_id.keys())
        for group in groups:
            posts = await self.get_posts_info(group)
            for post in posts:
                if post['attachments'] and 'text' in post:
                    id = int(group) + post['id']
                    post_text = post['text'] + "*//*" + group_id[group] + '*//*' + group[1:]
                    photo_urls = []
                    for attachment in post['attachments']:
                        if attachment['type'] == 'photo':
                            photo_info = attachment['photo']
                            photo_url = max(photo_info['sizes'], key=lambda x: x['height'])['url']
                            photo_urls.append(photo_url)
                    DBA = DBAlchemy()
                    photo_str = ""
                    if photo_urls:
                        photo_str = ",".join(photo_urls)

                        data = await DBA.add_new_data(id=id, text=post_text, photo=photo_str)
                        if not data:
                            continue





