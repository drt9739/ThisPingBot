import telebot
import json

from config import  TOKEN
from telebot import types

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton('📄 Список упоминаний'), types.KeyboardButton('📎 Команды'),
               types.KeyboardButton('💾 Настройки'))

    bot.send_message(message.chat.id, f'Привет *{message.chat.username}* 👋\n'
                                      f'В это боте вы можете подписываться на упоменания в чате твича\n\n'
                                      f'Чтобы создать/дополнить упоминания напишите '
                                      f'\n  `/create'
                                      f' <название канала> <упоминания>`', reply_markup=markup,
                     parse_mode='Markdown')


@bot.message_handler(commands=['create', 'создать'])
def create(message):
    if len(message.text.split()) >= 2:

        channel = message.text.split()[1]

    else:

        channel = None

    if len(message.text.split()) > 2:

        ping = message.text.split()[2:]

    else:

        ping = []
    print(ping)

    with open('base.txt', 'r', encoding='utf-8') as base:
        users = eval(base.read())

    if len(message.text.split()) == 1:

        bot.send_message(message.chat.id, f'Пожалуйста укажите канал и хотя бы одно упоминание')

    elif str(message.chat.id) in users['user_id'].keys() and ping != []:

        users['all_channel'].append(channel)
        users['user_id'][str(message.chat.id)]['channels'].append(channel)

        for el in ping:
            users['all_pings'].append(el)

            if el not in users['user_id'][str(message.chat.id)]['ping']:
                users['user_id'][str(message.chat.id)]['ping'].append(el)

            if el not in users['ping'].keys():

                users['ping'][el] = [message.chat.id]

            else:

                users['ping'][el].append(message.chat.id)

        bot.send_message(message.chat.id, f'*Успешно добавлены ✅*', parse_mode='Markdown')

    elif str(message.chat.id) not in users['user_id'].keys() and ping != []:

        users['user_id'][str(message.chat.id)] = {'ping': [x for x in ping], 'channels': [channel]}
        users['all_channel'].append(channel)

        for el in ping:
            if el not in users['all_pings']:
                users['all_pings'].append(el)

            if el not in users['ping'].keys():

                users['ping'][el] = [message.chat.id]

            else:

                users['ping'][el].append(message.chat.id)

        bot.send_message(message.chat.id, f'*Успешно добавлены ✅*', parse_mode='Markdown')

    elif not ping:

        bot.send_message(message.chat.id, f'*❌ Вы не указали упоминания*\n'
                                          f'Если вы хотите добавить канал/упоминания '
                                          f'пропришите `/add` или `/add_ping`', parse_mode='Markdown')

    print(users)

    with open('base.txt', 'w', encoding='utf-8') as p:
        json.dump(users, p, ensure_ascii=False)


@bot.message_handler(commands=['add'])
def add_channels(message):
    if len(message.text.split()) >= 2:
        channels = message.text.split()[1:]
    else:
        channels = None

    with open('base.txt', encoding='utf-8') as d:
        users = json.load(d)

    if channels is not None and str(message.chat.id) in users['user_id'].keys():

        for el in channels:

            if el not in users['user_id'][str(message.chat.id)]['channels']:
                users['user_id'][str(message.chat.id)]['channels'].append(el)

            if el not in users['all_channel']:
                users['all_channel'].append(el)

        bot.send_message(message.chat.id, f'*Успешно добавлены ✅*', parse_mode='Markdown')

    else:

        bot.send_message(message.chat.id, f'*Вы не указали ни одного канала, интересно почему 🤔*\n'
                                          f'Попробуйте указать хотя бы один канал', parse_mode='Markdown')

    with open('base.txt', 'w', encoding='utf-8') as p:
        json.dump(users, p, ensure_ascii=False)


@bot.message_handler(commands=['add_ping'])
def add_ping(message):
    with open('base.txt', encoding='utf-8') as d:
        users = json.load(d)

    if len(message.text.split()) >= 2:

        ping = message.text.split()[1:]

    else:

        ping = None

    if ping is not None and str(message.chat.id) in users['user_id'].keys():

        for el in ping:

            if el not in users['all_pings']:
                users['all_pings'].append(el)

            if el not in users['ping'].keys():

                users['ping'][el] = [message.chat.id]

            else:

                users['ping'][el].append(el)

            if el not in users['user_id'][str(message.chat.id)]['ping']:
                users['user_id'][str(message.chat.id)]['ping'].append(el)

        bot.send_message(message.chat.id, f'*Успешно добавлены ✅*', parse_mode='Markdown')

    else:

        if ping is None:

            bot.send_message(message.chat.id, 'Вы не ввели упоминания после команды 🤨')

        elif message.chat.id not in users['user_id'].keys():

            bot.send_message(message.chat.id, 'У вас не создано хотя бы одно упоминание.\n'
                                              'Пропишите `/create` чтобы создать упоминания', parse_mode='Markdown')

    with open('base.txt', 'w', encoding='utf-8') as p:
        json.dump(users, p, ensure_ascii=False)


@bot.message_handler(content_types='text')
def button(message):
    if message.text == '📄 Список упоминаний':

        with open('base.txt', encoding='utf-8') as d:
            base = json.load(d)
        print(base)

        if str(message.chat.id) in base['user_id'].keys():

            string = '*Ваши упоминания:*\n'

            for el in base['user_id'][str(message.chat.id)]['ping']:
                string += f' - `{el}`\n'

            string += f'\n*Каналы с отслеживание упомнианий:*\n'

            for el in base['user_id'][str(message.chat.id)]['channels']:
                string += f' - `{el}`\n'

            bot.send_message(message.chat.id, string, parse_mode='Markdown')

    elif message.text == '📎 Команды':

        bot.send_message(message.chat.id, f'*Вот все команды:*\n'
                                          f'`/create` - создаёт упоминания в указаном канале. Сначала идёт канал, '
                                          f'а потом упоминания (без запятых)\n'
                                          f'`/add` - добавляет каналы для упоминаний\n'
                                          f'`/add_ping` - добавляет упоминания', parse_mode='Markdown')

    elif message.text == '💾 Настройки':
        with open('base.txt', encoding='utf-8') as d:
            users = json.load(d)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        if message.chat.id not in users['ppl']:

            markup.add(types.KeyboardButton('Спец уведомление | OFF'), types.KeyboardButton(''),
                       types.KeyboardButton('⬅️Выход'))

        else:

            markup.add(types.KeyboardButton('Спец уведомление | ON'), types.KeyboardButton(''),
                       types.KeyboardButton('⬅️Выход'))

        bot.send_message(message.chat.id, f'Вы перешли в настройки \n'
                                          f'На данный момент доступна только настройка *Спец уведомления*\n\n'
                                          f'*Спец уведомление* - это уведомления предназначенные для получения '
                                          f'информации о старте предзаказа на ппл 🐸', reply_markup=markup,
                         parse_mode='Markdown')

        with open('base.txt', 'w', encoding='utf-8') as p:
            json.dump(users, p, ensure_ascii=False)

    elif message.text == '⬅️Выход':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(types.KeyboardButton('📄 Список упоминаний'), types.KeyboardButton('📎 Команды'),
                   types.KeyboardButton('💾 Настройки'))

        bot.send_message(message.chat.id, f'Вы вернули в главное меню', reply_markup=markup)

    elif message.text == 'Спец уведомление | OFF':

        with open('base.txt', encoding='utf-8') as d:
            users = json.load(d)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(types.KeyboardButton('Спец уведомление | ON'), types.KeyboardButton(''),
                   types.KeyboardButton('⬅️Выход'))

        if message.chat.id not in users['ppl']:
            users['ppl'].append(message.chat.id)

        bot.send_message(message.chat.id, f'Настройки изменены', reply_markup=markup)

        with open('base.txt', 'w', encoding='utf-8') as p:
            json.dump(users, p, ensure_ascii=False)

    elif message.text == 'Спец уведомление | ON':

        with open('base.txt', encoding='utf-8') as d:
            users = json.load(d)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(types.KeyboardButton('Спец уведомление | OFF'), types.KeyboardButton(''),
                   types.KeyboardButton('⬅️Выход'))

        if message.chat.id not in users['ppl']:
            users['ppl'].pop(message.chat.id)

        bot.send_message(message.chat.id, f'Настройки изменены', reply_markup=markup)

        with open('base.txt', 'w', encoding='utf-8') as p:
            json.dump(users, p, ensure_ascii=False)


bot.infinity_polling()
