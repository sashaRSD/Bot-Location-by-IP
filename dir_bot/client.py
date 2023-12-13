from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from dir_bot import create_bot
from dir_get import get_ip
import re, time
dp = create_bot.dp
bot = create_bot.bot

ID_ip = None
bool_ip = True
button = ['/Узнать_свой_ip_адрес']
contact = ['/Обратная_связь']
donat = ['/Поддержать']
kb = ReplyKeyboardMarkup(resize_keyboard=True).add(*button).add(*contact).insert(*donat)
button_cancel = ['/Удалить_ссылку_сейчас']
kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(*button_cancel)


@dp.message_handler(commands=['start'])
async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, f'Добрый день, {message.from_user.first_name}!', reply_markup=kb)
        await bot.send_message(message.from_user.id, f'Вы можете узнать информацию о вашем ip-адресе.\n'
                                                     f'Для этого отправьте его мне.')
    except:
        await message.delete()
        await message.reply('Напишите мне в личные сообщения')

@dp.message_handler(commands=['Обратная_связь'])
async def commands_contact(message: types.Message):
    await message.answer('Наши контактные данные: \n'
                         'Электронная почта - kaa.1999@mail.ru \n'
                         'Username Telegram - @sasha_rsd')


@dp.message_handler(commands=['help'])
async def commands_help(message: types.Message):
    await bot.send_message(message.from_user.id,  f'Вы можете узнать информацию о вашем ip-адресе.\n'
                                                  f'Для этого отправьте его мне.', reply_markup=kb)


@dp.message_handler(commands=['Поддержать'])
async def commands_help(message: types.Message):
    text = 'Жми сюда!'
    url = 'https://www.tinkoff.ru/cf/71ARxuIBdob'
    url_button = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text=text, url=url))
    await message.answer('Поддержать автора копейкой ;)', reply_markup=url_button)


@dp.message_handler(commands=['cancel', 'Удалить_ссылку_сейчас'])
async def commands_help(message: types.Message):
    global bool_ip, ID_ip
    if ID_ip == message.from_user.id:
        bool_ip = True
        ID_ip = None
        await message.answer(f'Я не успел узнать ваш ip-адрес...\n'
                             f'Попробуйте еще раз ;)', reply_markup=kb)
    else:
        await message.answer('Ошибка доступа!')


@dp.message_handler(commands=['Узнать_свой_ip_адрес'])
async def commands_help(message: types.Message):
    global bool_ip, ID_ip
    if bool_ip:
        bool_ip = False
        ID_ip = message.from_user.id
        time0 = get_ip.scraping('Time')
        await bot.send_message(message.from_user.id,  f'Перейдите по ссылке в течение 1 минуты.\n'
                                                      f'После этого мы отправим вам данные.\n'
                                                      f'Если передумали: /cancel', reply_markup=kb_cancel)
        text = 'Ссылка'
        url = 'https://iplogger.com/2VHUh4'
        url_button = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text=text, url=url))
        time_button = await message.answer('Для перехода по ссылке - осталось 60 секунд.', reply_markup=url_button)
        for num in range(60):
            time.sleep(1)
            if time0 != get_ip.scraping('Time'):
                data = get_ip.get_data(None)
                await message.answer(data[0], reply_markup=kb)
                if data[1] and data[2]:
                    await bot.send_location(message.from_user.id, data[1], data[2])
                await bot.edit_message_text(chat_id=message.chat.id, message_id=time_button.message_id,
                                            text=f'IP-адрес успешно определен!', reply_markup=None)
                break
            else:
                if bool_ip:
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=time_button.message_id,
                                                text=f'Cсылка удалена!', reply_markup=None)
                    return
                if num != 59:
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=time_button.message_id,
                                                text=f'Для перехода по ссылке - осталось {59 - num} секунд.', reply_markup=url_button)
                else:
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=time_button.message_id,
                                                text=f'Время вышло, ссылка удалена...\nПовторите попытку!', reply_markup=None)
        bool_ip = True
        ID_ip = None
    else:
        await message.answer('Бот уже узнает ip-адрес у другого человека...\nПовторите запрос позжде!')


@dp.message_handler(lambda message: re.findall(r"([0-9]{1,3}[\.]){3}[0-9]{1,3}", message.text))
async def commands_help(message: types.Message):
    for ip in message.text.split('.'):
        if len(ip) > 3:
            await message.answer('ip-адрес введен неверно...\nПовторите попытку!')
            return
    data = get_ip.get_data({"[IP]": f'{message.text}'})
    await message.answer(data[0], reply_markup=kb)
    if data[1] and data[2]:
        await bot.send_location(message.from_user.id, data[1], data[2])


@dp.message_handler()
async def commands_help(message: types.Message):
        await bot.send_message(message.from_user.id, f'Я вас не понимаю :(\n'
                                                     f'Отправьте мне ip-адрес\n'
                                                     f'Пример: 92.168.0.1', reply_markup=kb)
