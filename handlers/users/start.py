import asyncio
from asyncio import sleep
from pprint import pprint
from data.config import VK_TOKEN, GROUP_IDs

import requests
from aiogram import types

from buttons.key_board import kb_start
from data.config import CHANAL_ID, DEPLOY, DEPLOY_POST, GROUP_IDs
from handlers.workers.control_db import DBAlchemy
from handlers.workers.controle_vk import VK_Manager
from loader import dp



@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(
        "Кнопка ЗАПУСК запускает бот, который проверяет группу Imperia's Wheels MCC на предмет новых постов",
        reply_markup=kb_start)


@dp.message_handler(text="ЗАПУСК", content_types=types.ContentType.TEXT)
async def start_program(message:types.Message):
    await message.answer("Запуск программы")
    db = DBAlchemy()
    await db.create_db()
    vk_m = VK_Manager(token=VK_TOKEN)
    while True:

        await vk_m.add_post(GROUP_IDs)
        posts = await db.get_not_publish_post()
        for post in posts:
            text, title, href = post.text.split('*//*')
            text_post = f"<b>{title}</b>\n\n{text}\n\nhttps://vk.com/public{href}"

            if post.photo:
                media = types.MediaGroup()
                links = post.photo.split(',')
                for i, link in enumerate(links):
                    if i == (len(links) - 1):
                        media.attach_photo(types.InputFile.from_url(link), caption=text_post[:1024],
                                           parse_mode=types.ParseMode.HTML)
                    else:
                        media.attach_photo(types.InputFile.from_url(link))
                try:
                    await message.bot.send_media_group(chat_id=CHANAL_ID, media=media)
                    await db.update_publish_value(id=post.id)
                    await sleep(15)
                except asyncio.TimeoutError:
                    print('Запрос занял слишком много времени. Время ожидания истекло.')
                    await sleep(10)
                    continue
                except Exception as e:
                    print(f'Произошла ошибка при отправке сообщения: {e}')
                    continue
                    await sleep(10)
            else:
                try:
                    await message.bot.send_message(chat_id=CHANAL_ID, text=text_post,
                                                   parse_mode=types.ParseMode.HTML)
                    await db.update_publish_value(id=post.id)
                except asyncio.TimeoutError:
                    print('Запрос занял слишком много времени. Время ожидания истекло.')
                    continue
                    await sleep(10)
                except Exception as e:
                    print(f'Произошла ошибка при отправке сообщения: {e}')
                    continue
                    await sleep(10)

        print(f"DEPLOY: {DEPLOY} сек.",)
        await db.delete_total_records(150)
        await sleep(DEPLOY)




