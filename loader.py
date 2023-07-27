from aiogram import types, Dispatcher, Bot


from data.config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage


TOKEN = TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
