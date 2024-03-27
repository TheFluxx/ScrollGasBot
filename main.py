import logging

from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from data.config import BOT_TOKEN
from db_api.database import create_base
from handlers.echo import register_echo
from handlers.client import register_command_start
from utils.set_default_commands import set_default_commands

def setup_handlers(dp: Dispatcher):
    register_command_start(dp)
    register_echo(dp)



async def on_startup(dp: Dispatcher):
    setup_handlers(dp)
    await set_default_commands(dp)
    await create_base()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, on_startup=on_startup)
