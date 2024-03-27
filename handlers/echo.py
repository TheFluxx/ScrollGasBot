from aiogram import Dispatcher
from aiogram.types import Message
from keyboards.client_kb import start_kb

async def echo(message: Message):
    await message.answer('<b>❌ Что-то пошло не так, повторите действие заново!</b>', reply_markup=start_kb)


def register_echo(dp: Dispatcher):
    dp.register_message_handler(echo, state='*')
