from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from db_api.db_commands.user_commands import add_user, read_users, select_user, add_upper_limit, get_limit, set_user_language
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.client_kb import start_kb, language_kb, start_kb_en
from datetime import datetime, timedelta
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from data.config import BOT_TOKEN

from handlers.gas import get_gas_price_gwei
from data.config import CHAT_ID


bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)


class FSMGasPrice(StatesGroup):
    gasprice = State()
    gasprice_en = State()




async def process_start_command(message: types.Message):
    referral_id = str(message.text[7:])
    username = message.from_user.username
    if username is None:
        username = message.from_user.first_name
    
    if await select_user(message.from_user.id) == None:
        await add_user(message.from_user.id, username, referral_id, 1.0, 'EN')

#         await message.answer(
#             """
#     Поздравляем, вы зарегистрированы!
#             """,
#             reply_markup=start_kb
#         )
#     else:
#         await message.answer(
#             """
# Вы уже были зарегистрированы!
#             """,
#             reply_markup=start_kb
#         )
    await message.answer("🌏 Language", reply_markup=language_kb)


async def get_gas(message: types.Message, state: FSMContext):
    await state.finish()
    gas_price_gwei = get_gas_price_gwei()
    if gas_price_gwei <= 0.4: 
        flag = '🟩'
    elif gas_price_gwei >= 1:
        flag = '🟥'
    else:
        flag = '🟧'

        await message.answer(text=f"""<b>SCROLL GAS: </b>
{gas_price_gwei} Gwei {flag}

<b><a href="https://t.me/ScrollGas">Scroll Gas Tracker</a></b>""", parse_mode='HTML')


async def get_gas_en(message: types.Message, state: FSMContext):
    await state.finish()
    gas_price_gwei = get_gas_price_gwei()
    if gas_price_gwei <= 0.4: 
        flag = '🟩'
    elif gas_price_gwei >= 1:
        flag = '🟥'
    else:
        flag = '🟧'

        await message.answer(text=f"""<b>SCROLL GAS: </b>
{gas_price_gwei} Gwei {flag}

<b><a href="https://t.me/ScrollGas">Scroll Gas Tracker</a></b>""", parse_mode='HTML')


async def settings_language(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🌏 Выберите язык", reply_markup=language_kb)


async def check_subscriptions(wait_for):
    gas_price_gwei = get_gas_price_gwei()

    if gas_price_gwei <= 0.4: 
        flag = '🟩'
    elif gas_price_gwei >= 1:
        flag = '🟥'
    else:
        flag = '🟧'

    while True:
        await bot.send_message(chat_id=CHAT_ID, text=f"""<b>SCROLL GAS: </b>
{gas_price_gwei} Gwei {flag}

<b><a href="https://t.me/ScrollGas">Scroll Gas Tracker</a></b>""", parse_mode='HTML')

        for user in await read_users():
            if gas_price_gwei <= user.notification_upper_limit:
                await bot.send_message(user.telegram_id, f"""<b>SCROLL GAS: </b>
{gas_price_gwei} Gwei {flag}

<b><a href="https://t.me/ScrollGas">Scroll Gas Tracker</a></b>""", parse_mode='HTML')




        await asyncio.sleep(wait_for)



async def settings_notification(message: types.Message, state: FSMContext):
    await state.finish()
    settings_kb = InlineKeyboardMarkup(row_width=3)

    limit = float(await get_limit(message.from_user.id))
    if limit == 0.4:
        settings_kb.row(InlineKeyboardButton(text='Низкая✅',
            callback_data=f'settings_low'), InlineKeyboardButton(text='Средняя',
            callback_data=f'settings_average'),InlineKeyboardButton(text='Высокая',
            callback_data=f'settings_high'))
        settings_kb.add(InlineKeyboardButton(text='⚙️ Своя цена',
        callback_data=f'wait_gas_price'))
    
    elif limit == 0.6:
        settings_kb.row(InlineKeyboardButton(text='Низкая',
            callback_data=f'settings_low'), InlineKeyboardButton(text='Средняя✅',
            callback_data=f'settings_average'),InlineKeyboardButton(text='Высокая',
            callback_data=f'settings_high'))
        settings_kb.add(InlineKeyboardButton(text='⚙️ Своя цена',
        callback_data=f'wait_gas_price'))

    elif limit == 1:
        settings_kb.row(InlineKeyboardButton(text='Низкая',
            callback_data=f'settings_low'), InlineKeyboardButton(text='Средняя',
            callback_data=f'settings_average'),InlineKeyboardButton(text='Высокая✅',
            callback_data=f'settings_high'))
        settings_kb.add(InlineKeyboardButton(text='⚙️ Своя цена',
        callback_data=f'wait_gas_price'))

    else:
        settings_kb.row(InlineKeyboardButton(text='Низкая',
            callback_data=f'settings_low'), InlineKeyboardButton(text='Средняя',
            callback_data=f'settings_average'),InlineKeyboardButton(text='Высокая',
            callback_data=f'settings_high'))
        settings_kb.add(InlineKeyboardButton(text=f'✅ Своя цена - {limit}',
        callback_data=f'wait_gas_price'))


    await message.answer(f"""🔄 *Вы будете получать уведомления, когда цена на газ станет ниже*""".replace('.', '\.'), parse_mode='MarkdownV2', reply_markup=settings_kb)


async def add_criterion_of_notification(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    if call.data == 'settings_low':
        await add_upper_limit(call.from_user.id, 0.4)

    elif call.data == 'settings_average':
        await add_upper_limit(call.from_user.id, 0.6)

    elif call.data == 'settings_high':
        await add_upper_limit(call.from_user.id, 1)

    settings_kb = InlineKeyboardMarkup(row_width=3)

    limit = float(await get_limit(call.from_user.id))
    if limit == 0.4:
        settings_kb.row(InlineKeyboardButton(text='Низкая✅',
            callback_data=f'settings_low'), InlineKeyboardButton(text='Средняя',
            callback_data=f'settings_average'),InlineKeyboardButton(text='Высокая',
            callback_data=f'settings_high'))
        settings_kb.add(InlineKeyboardButton(text='⚙️ Своя цена',
        callback_data=f'wait_gas_price'))
    
    elif limit == 0.6:
        settings_kb.row(InlineKeyboardButton(text='Низкая',
            callback_data=f'settings_low'), InlineKeyboardButton(text='Средняя✅',
            callback_data=f'settings_average'),InlineKeyboardButton(text='Высокая',
            callback_data=f'settings_high'))
        settings_kb.add(InlineKeyboardButton(text='⚙️ Своя цена',
        callback_data=f'wait_gas_price'))

    elif limit == 1:
        settings_kb.row(InlineKeyboardButton(text='Низкая',
            callback_data=f'settings_low'), InlineKeyboardButton(text='Средняя',
            callback_data=f'settings_average'),InlineKeyboardButton(text='Высокая✅',
            callback_data=f'settings_high'))
        settings_kb.add(InlineKeyboardButton(text='⚙️ Своя цена',
        callback_data=f'wait_gas_price'))

    else:
        settings_kb.row(InlineKeyboardButton(text='Низкая',
            callback_data=f'settings_low'), InlineKeyboardButton(text='Средняя',
            callback_data=f'settings_average'),InlineKeyboardButton(text='Высокая',
            callback_data=f'settings_high'))
        settings_kb.add(InlineKeyboardButton(text=f'✅ Своя цена - {limit}',
        callback_data=f'wait_gas_price'))

    user_limit = await get_limit(call.from_user.id)

    await call.message.edit_text(f"""🔄 *Вы будете получать уведомления, когда цена на газ станет ниже:*""".replace('.', '\.'), parse_mode='MarkdownV2', reply_markup=settings_kb)




async def wait_gas_price(call: types.CallbackQuery):
    await call.message.answer(f"""<b>⛽️ Укажите цену за газ, ниже которой хотите получать уведомления:</b>""", parse_mode="HTML")
    await FSMGasPrice.gasprice.set()


async def set_gas_price(message: types.Message, state: FSMContext):
    try:
        await add_upper_limit(message.from_user.id, float(message.text))
        
        settings_kb = InlineKeyboardMarkup(row_width=3)
        
        limit = float(await get_limit(message.from_user.id))
        
        if limit == 0.4:
            settings_kb.row(InlineKeyboardButton(text='Низкая✅',
                callback_data=f'settings_low'), InlineKeyboardButton(text='Средняя',
                callback_data=f'settings_average'),InlineKeyboardButton(text='Высокая',
                callback_data=f'settings_high'))
            settings_kb.add(InlineKeyboardButton(text='⚙️ Своя цена',
            callback_data=f'wait_gas_price'))
        
        elif limit == 0.6:
            settings_kb.row(InlineKeyboardButton(text='Низкая',
                callback_data=f'settings_low'), InlineKeyboardButton(text='Средняя✅',
                callback_data=f'settings_average'),InlineKeyboardButton(text='Высокая',
                callback_data=f'settings_high'))
            settings_kb.add(InlineKeyboardButton(text='⚙️ Своя цена',
            callback_data=f'wait_gas_price'))

        elif limit == 1:
            settings_kb.row(InlineKeyboardButton(text='Низкая',
                callback_data=f'settings_low'), InlineKeyboardButton(text='Средняя',
                callback_data=f'settings_average'),InlineKeyboardButton(text='Высокая✅',
                callback_data=f'settings_high'))
            settings_kb.add(InlineKeyboardButton(text='⚙️ Своя цена',
            callback_data=f'wait_gas_price'))

        else:
            settings_kb.row(InlineKeyboardButton(text='Низкая',
                callback_data=f'settings_low'), InlineKeyboardButton(text='Средняя',
                callback_data=f'settings_average'),InlineKeyboardButton(text='Высокая',
                callback_data=f'settings_high'))
            settings_kb.add(InlineKeyboardButton(text=f'✅ Своя цена - {limit}',
            callback_data=f'wait_gas_price'))
            user_limit = await get_limit(message.from_user.id)
            await state.finish()
            await message.answer(f"""🔄 *Вы будете получать уведомления, когда цена на газ станет ниже:*""".replace('.', '\.'), parse_mode='MarkdownV2', reply_markup=settings_kb)
    except:
        await message.answer("⚠️ Вы ввели недопустимое значение, попробуйте еще раз:")



async def set_language(call: types.CallbackQuery):
    await call.message.delete()
    if call.data == 'language_ru':
        await set_user_language(call.from_user.id, 'RU')
        await call.message.answer('🌏 Поздравляем! Вы установили Русский язык!', reply_markup=start_kb)
    if call.data == 'language_en':
        await set_user_language(call.from_user.id, 'RU')
        await call.message.answer('🌏 Congratulations! You set the English language!', reply_markup=start_kb_en)



##########

async def settings_notification_en(message: types.Message, state: FSMContext):
    await state.finish()
    settings_kb = InlineKeyboardMarkup(row_width=3)

    limit = float(await get_limit(message.from_user.id))
    if limit == 0.4:
        settings_kb.row(InlineKeyboardButton(text='Low✅',
            callback_data=f'en_settings_low'), InlineKeyboardButton(text='Average',
            callback_data=f'en_settings_average'),InlineKeyboardButton(text='High',
            callback_data=f'en_settings_high'))
        settings_kb.add(InlineKeyboardButton(text='⚙️ Set a price',
        callback_data=f'en_wait_gas_price'))
    
    elif limit == 0.6:
        settings_kb.row(InlineKeyboardButton(text='Low',
            callback_data=f'en_settings_low'), InlineKeyboardButton(text='Average✅',
            callback_data=f'en_settings_average'),InlineKeyboardButton(text='High',
            callback_data=f'en_settings_high'))
        settings_kb.add(InlineKeyboardButton(text='⚙️ Set a price',
        callback_data=f'en_wait_gas_price'))

    elif limit == 1:
        settings_kb.row(InlineKeyboardButton(text='Low',
            callback_data=f'en_settings_low'), InlineKeyboardButton(text='Average',
            callback_data=f'en_settings_average'),InlineKeyboardButton(text='High✅',
            callback_data=f'en_settings_high'))
        settings_kb.add(InlineKeyboardButton(text='⚙️ Set a price',
        callback_data=f'en_wait_gas_price'))

    else:
        settings_kb.row(InlineKeyboardButton(text='Low',
            callback_data=f'en_settings_low'), InlineKeyboardButton(text='Average',
            callback_data=f'en_settings_average'),InlineKeyboardButton(text='High',
            callback_data=f'en_settings_high'))
        settings_kb.add(InlineKeyboardButton(text=f'✅ Set a price - {limit}',
        callback_data=f'en_wait_gas_price'))


    await message.answer(f"""🔄 *You will receive notifications when the gas price is lower then:*""".replace('.', '\.'), parse_mode='MarkdownV2', reply_markup=settings_kb)


async def add_criterion_of_notification_en(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    if call.data == 'en_settings_low':
        await add_upper_limit(call.from_user.id, 0.4)

    elif call.data == 'en_settings_average':
        await add_upper_limit(call.from_user.id, 0.6)

    elif call.data == 'en_settings_high':
        await add_upper_limit(call.from_user.id, 1)

    settings_kb = InlineKeyboardMarkup(row_width=3)

    limit = float(await get_limit(call.from_user.id))
    if limit == 0.4:
        settings_kb.row(InlineKeyboardButton(text='Low✅',
            callback_data=f'en_settings_low'), InlineKeyboardButton(text='Average',
            callback_data=f'en_settings_average'),InlineKeyboardButton(text='High',
            callback_data=f'en_settings_high'))
        settings_kb.add(InlineKeyboardButton(text='⚙️ Set a price',
        callback_data=f'en_wait_gas_price'))
    
    elif limit == 0.6:
        settings_kb.row(InlineKeyboardButton(text='Low',
            callback_data=f'en_settings_low'), InlineKeyboardButton(text='Average✅',
            callback_data=f'en_settings_average'),InlineKeyboardButton(text='High',
            callback_data=f'en_settings_high'))
        settings_kb.add(InlineKeyboardButton(text='⚙️ Set a price',
        callback_data=f'en_wait_gas_price'))

    elif limit == 1:
        settings_kb.row(InlineKeyboardButton(text='Low',
            callback_data=f'en_settings_low'), InlineKeyboardButton(text='Average',
            callback_data=f'en_settings_average'),InlineKeyboardButton(text='High✅',
            callback_data=f'en_settings_high'))
        settings_kb.add(InlineKeyboardButton(text='⚙️ Set a price',
        callback_data=f'en_wait_gas_price'))

    else:
        settings_kb.row(InlineKeyboardButton(text='Low',
            callback_data=f'en_settings_low'), InlineKeyboardButton(text='Average',
            callback_data=f'en_settings_average'),InlineKeyboardButton(text='High',
            callback_data=f'en_settings_high'))
        settings_kb.add(InlineKeyboardButton(text=f'✅ Set a price - {limit}',
        callback_data=f'en_wait_gas_price'))

    user_limit = await get_limit(call.from_user.id)

    await call.message.edit_text(f"""🔄 *You will receive notifications when the gas price is lower then:*""".replace('.', '\.'), parse_mode='MarkdownV2', reply_markup=settings_kb)




async def wait_gas_price_en(call: types.CallbackQuery):
    await call.message.answer(f"""<b>⛽️ Specify the gas price below which you want to receive notifications:</b>""", parse_mode="HTML")
    await FSMGasPrice.gasprice_en.set()


async def set_gas_price_en(message: types.Message, state: FSMContext):
    try:
        await add_upper_limit(message.from_user.id, float(message.text))
        
        settings_kb = InlineKeyboardMarkup(row_width=3)
        
        limit = float(await get_limit(message.from_user.id))
        
        if limit == 0.4:
            settings_kb.row(InlineKeyboardButton(text='Low✅',
                callback_data=f'en_settings_low'), InlineKeyboardButton(text='Average',
                callback_data=f'en_settings_average'),InlineKeyboardButton(text='High',
                callback_data=f'en_settings_high'))
            settings_kb.add(InlineKeyboardButton(text='⚙️ Set a price',
            callback_data=f'en_wait_gas_price'))
        
        elif limit == 0.6:
            settings_kb.row(InlineKeyboardButton(text='Low',
                callback_data=f'en_settings_low'), InlineKeyboardButton(text='Average✅',
                callback_data=f'en_settings_average'),InlineKeyboardButton(text='High',
                callback_data=f'en_settings_high'))
            settings_kb.add(InlineKeyboardButton(text='⚙️ Set a price',
            callback_data=f'en_wait_gas_price'))

        elif limit == 1:
            settings_kb.row(InlineKeyboardButton(text='Low',
                callback_data=f'en_settings_low'), InlineKeyboardButton(text='Average',
                callback_data=f'en_settings_average'),InlineKeyboardButton(text='High✅',
                callback_data=f'en_settings_high'))
            settings_kb.add(InlineKeyboardButton(text='⚙️ Set a price',
            callback_data=f'en_wait_gas_price'))

        else:
            settings_kb.row(InlineKeyboardButton(text='Low',
                callback_data=f'en_settings_low'), InlineKeyboardButton(text='Average',
                callback_data=f'en_settings_average'),InlineKeyboardButton(text='High',
                callback_data=f'en_settings_high'))
            settings_kb.add(InlineKeyboardButton(text=f'✅ Set a price - {limit}',
            callback_data=f'en_wait_gas_price'))

        user_limit = await get_limit(message.from_user.id)
        await state.finish()
        await message.answer(f"""🔄 *You will receive notifications when the gas price is lower then::*""".replace('.', '\.'), parse_mode='MarkdownV2', reply_markup=settings_kb)
    except:
        await message.answer("⚠️ The value you entered is invalid, please try again:")


async def settings_language_en(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🌏 Choose language", reply_markup=language_kb)







def register_command_start(dp: Dispatcher):
    loop = asyncio.get_event_loop()
    loop.create_task(check_subscriptions(60))
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(settings_language, Text("🌐 Язык"), state='*')
    dp.register_message_handler(settings_language_en, Text("🌐 Language"), state='*')
    dp.register_message_handler(get_gas, Text("⛽️ Узнать газ"), state='*')
    dp.register_message_handler(get_gas_en, Text("⛽️ Get gas value"), state='*')
    dp.register_message_handler(settings_notification, Text("⚙️Настройки"), state='*')
    dp.register_message_handler(settings_notification_en, Text("⚙️ Settings"), state='*')
    dp.register_callback_query_handler(add_criterion_of_notification, lambda x: x.data and x.data.startswith('settings_'), state='*')
    dp.register_callback_query_handler(wait_gas_price, Text("wait_gas_price"))
    dp.register_message_handler(set_gas_price, state=FSMGasPrice.gasprice)
    dp.register_callback_query_handler(set_language, lambda x: x.data and x.data.startswith('language_'), state='*')
    dp.register_callback_query_handler(add_criterion_of_notification_en, lambda x: x.data and x.data.startswith('en_settings_'), state='*')
    dp.register_callback_query_handler(wait_gas_price_en, Text("en_wait_gas_price"))
    dp.register_message_handler(set_gas_price_en, state=FSMGasPrice.gasprice_en)