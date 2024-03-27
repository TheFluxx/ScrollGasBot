from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button = KeyboardButton('⚙️Настройки')
button2 = KeyboardButton('🌐 Язык')
button3 = KeyboardButton('⛽️ Узнать газ')

start_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button3).row(button, button2)


button_en = KeyboardButton('⚙️ Settings')
button2_en = KeyboardButton('🌐 Language')
button3_en = KeyboardButton('⛽️ Get gas value')

start_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).add(button3_en).row(button_en, button2_en)

language_kb = InlineKeyboardMarkup(row_width=1)

language_kb.add(InlineKeyboardButton(text='RU', callback_data=f'language_ru'), 
                InlineKeyboardButton(text='EN',callback_data=f'language_en'))