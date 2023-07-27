from asyncio import sleep
from pprint import pprint

import requests
from aiogram import types

from buttons.key_board import kb_start
from data.config import CHANAL_ID, DEPLOY, DEPLOY_POST, GROUP_IDs
from loader import dp
from handlers.workers.manager import AdminDB, get_all_well


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(
        "Кнопка ЗАПУСК запускает бот, который проверяет группу Imperia's Wheels MCC на предмет новых постов",
        reply_markup=kb_start)


@dp.message_handler(text="ЗАПУСК", content_types=types.ContentType.TEXT)
async def go(message: types.Message):
    adminDB = AdminDB()

    while True:
        await adminDB.delete_last_records_if_exceed_limit()
        await sleep(DEPLOY)
        await get_all_well(GROUP_IDs)
        posts = await adminDB.get_post_not_publish()

        if posts:
            for post in posts:

                text = post[1]
                media = types.MediaGroup()
                if post[2]:
                    links = post[2].split(',')
                    for i, link in enumerate(links):
                        print(link)
                        print('*'*30)
                        if i == (len(links) - 1):
                            text_post = f"<b>Imperia's Wheels MCC</b>\n\n{text}"
                            media.attach_photo(types.InputFile.from_url(link), caption=text_post,
                                               parse_mode=types.ParseMode.HTML)
                        else:
                            media.attach_photo(types.InputFile.from_url(link))
                    await message.bot.send_media_group(chat_id=CHANAL_ID, media=media)
                else:
                    text_post = f"<b>Imperia's Wheels MCC</b>\n\n{text}"
                    await message.bot.send_message(chat_id=CHANAL_ID, text=text_post, parse_mode=types.ParseMode.HTML)
                await adminDB.publish_post(post[0])
                await sleep(DEPLOY_POST)
        else:
            pass

