import telebot

from twitch.twitch_listen import Bot
from config import TOKEN


def main():
    tg_bot = telebot.TeleBot(TOKEN)

    with open('telegram/base.txt') as d:
        users = eval(d.read())

    all = users['all_channel']
    twitch_bot = Bot(users['all_channel'])
    twitch_bot.add_ping(users['all_pings'])

    while True:
        with open('telegram/base.txt') as d:
            users = eval(d.read())

        res, spisok = twitch_bot.is_ping()

        if set(users['all_channel']) - set(all):
            pass
        print(spisok)
        if res:
            send = []
            if 'предзаказ' in spisok['ping']:
                for el in users['ppl']:
                    tg_bot.send_message(el, f'*Возможно наступил предзаказ!!*'
                                            f' Вот сообщение пользователя *{spisok["user"]}*:'
                                            f'\n*{spisok["message"]}*', parse_mode='Markdown')

            else:
                for el in spisok['ping']:

                    ids = users['ping'][el]
                    print(ids)

                    for i in ids:
                        print(i)
                        if spisok['channel'].split()[0] in users['user_id'][str(i)]['channels'] and i not in send:
                            print(i)
                            tg_bot.send_message(i,
                                                f'Вас упомянул пользователь *{spisok["user"]}* в чате'
                                                f' *{spisok["channel"]}*\n\n'
                                                f'Вот его сообщение: '
                                                f'*{spisok["message"]}*', parse_mode='Markdown')
                            send.append(i)

                else:
                    send.clear()


if __name__ == '__main__':
    main()
