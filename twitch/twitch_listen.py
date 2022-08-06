import re
import time

from socket import socket

import config


class Bot:
    def __init__(self, token: str, nickname: str, channels: list, default_channel=None):
        self.token = token
        self.nickname = nickname
        self.channels = channels
        self.pings = []
        self.bot = socket()
        if default_channel is not None:
            self.default_channel = default_channel

        self.bot.connect(('irc.twitch.tv', 6667))
        self.bot.send("PASS {}\r\n".format(token).encode("utf-8"))
        self.bot.send("NICK {}\r\n".format(nickname).encode("utf-8"))

        for channel in channels:
            self.bot.send("JOIN #{}\r\n".format(channel).encode("utf-8"))

    def connect(self, channels):
        for channel in channels:
            self.channels.append(channel)
            self.bot.send("JOIN #{}\r\n".format(channel).encode("utf-8"))

    def reconnect(self):
        self.bot = socket()
        self.bot.connect(('irc.twitch.tv', 6667))
        self.bot.send("PASS {}\r\n".format(self.token).encode("utf-8"))
        self.bot.send("NICK {}\r\n".format(self.nickname).encode("utf-8"))

        for channel in self.channels:
            self.bot.send("JOIN #{}\r\n".format(channel).encode("utf-8"))

    def get_update(self):
        try:
            response = self.bot.recv(2048).decode("utf-8")
        except ConnectionResetError:
            time.sleep(10)
            response = self.bot.recv(2048).decode('utf-8')

        if response == "PING :tmi.twitch.tv\r\n":
            self.bot.send("POND :tmi.twitch.tv\r\n".encode("utf-8"))

        elif f'#tmi.twitch.tv 421 {self.nickname} POND' not in response:
            username = re.search(r"\w+", response).group(0)
            message = ' '.join(str(response).split(':')[2:]).strip('\n\r')
            channel = str(response).split(':')[1].split('#')[-1]
            result = {'username': username,
                      'message': message,
                      'channel': channel}
            return result
        else:
            return None

    def add_pings(self, pings: list):
        for ping in pings:
            self.pings.append(ping)

    def is_ping(self):
        message = self.get_update()
        tg_message = f'https://api.telegram.org/bot{config.TOKEN}/getUpdates'
        try:
            if set(self.pings) & set(message['message'].split()) and message is not None:
                message['ping'] = list(set(self.pings) & set(message['message'].split()))
                return True, message
            else:
                return False, {}

        except TypeError:
            return False, {}

    def send(self, message, channel=None):
        if channel is None:
            channel = self.default_channel
        string = f"PRIVMSG #{channel} :{message}\r\n"
        string_as_bytes = str.encode(string)

        self.bot.send(string_as_bytes)
