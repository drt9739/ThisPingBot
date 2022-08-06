import telebot
import config
import json
import requests

from twitch.twitch_listen import Bot


def main():
    with open('telegram/base.txt', 'r', encoding='utf-8') as d:
        users = eval(d.read())

    bot = Bot(config.PASS, config.NICK, users['all_channel'])
    bot.add_pings(users['all_pings'])
    telegram = telebot.TeleBot(config.TOKEN)

    while True:
        flag, message = bot.is_ping()
        last_id = 0
        tg_message = requests.get(f'https://api.telegram.org/bot{config.TOKEN}/getUpdates').json()['result'][-1]
        if '/create' in tg_message['text'] or '/add' in tg_message['text'] or '/add_ping' in tg_message['text'] \
                and last_id != tg_message['message']['id']:
            last_id = tg_message['message']['id']
            with open('telegram/base.txt', 'r', encoding='utf-8') as d:
                users = eval(d.read())
            bot.connect(list(set(users['all_channel']) - set(bot.channels)))
            bot.add_pings(list(set(users['all_pings']) - set(bot.pings)))

        if flag:
            send = []
            for ping in message['ping']:
                for user_id in users[ping]:

                    if message['channel'] in users['user_id'][str(id)]['channels'] and id not in send:
                        bot.send(user_id,
                                 f'Вас упомянул пользователь {message["username"]} в чате {message["channel"]} \n\n'
                                 f'Вот его сообщение: {message["message"]}')
                        send.append(user_id)
            else:
                send.clear()


if __name__ == '__main__':
    main()
