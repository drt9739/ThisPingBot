from socket import socket
import re
import requests
import json

import config
import time


class Bot:
    def __init__(self, channel):
        self.s = socket()
        self.s.connect(('irc.twitch.tv', 6667))
        self.s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
        self.s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
        self.channels = channel[0]

        for el in channel:

            self.s.send("JOIN #{}\r\n".format(el).encode("utf-8"))

        self.chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
        self.ppl = ['pooshka', 'pwgood', 'rilaveon', 'dremoavnd', 'drt_s_s']
        self.ping = []

    def connect(self, channel):
        for el in channel:

            self.s.send("JOIN #{}\r\n".format(el).encode("utf-8"))

    def reconnect(self):
        time.sleep(5)
        self.s.connect(('irc.twitch.tv', 6667))
        self.s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
        self.s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))

        for el in self.channels:

            self.s.send("JOIN #{}\r\n".format(el).encode("utf-8"))

        self.chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

    def mess(self):
        try:

            try:

                response = self.s.recv(2048).decode("utf-8")

            except ConnectionResetError:

                response = self.s.recv(2048).decode("utf-8")

            if response == "PING :tmi.twitch.tv\r\n":

                self.s.send("POND :tmi.twitch.tv\r\n".encode("utf-8"))

            else:

                username = re.search(r"\w+", response).group(0)
                message = self.chat_message.sub("", response)

                if '#' in response:

                    channel = response.split('#')[1].split(':')[0]
                    flag = True

                else:

                    flag = False
                    channel = None

                if flag:

                    return True, {'channel': channel,
                                  'user': username,
                                  'message': message}
                else:

                    return False, {}

        except ConnectionAbortedError:

            self.reconnect()

    def send(self, message: str):
        string = f"PRIVMSG #{self.channels[0]} :{message}\r\n"
        string_as_bytes = str.encode(string)
        self.s.send(string_as_bytes)

    def loop(self):
        while True:

            try:

                user, mess, req = self.mess()

            except TypeError:

                user, mess, req = self.mess()

            print(req)

    def add_ping(self, args):
        for el in args:

            self.ping.append(el)

    def is_ping(self):
        try:

            res, spisok = self.mess()

        except TypeError:

            res, spisok = self.mess()

        if res:

            if set(self.ping) & set(spisok['message'].lower().split()):

                return True, {'channel': spisok['channel'],
                              'user': spisok['user'],
                              'message': spisok['message'],
                              'ping': list(set(self.ping) & set(spisok['message'].lower().split()))}

            elif 'предзаказ' in spisok['message'].lower().split() and spisok['user'] in self.ppl and\
                    spisok['channel'] == 'pwgood ':

                return True, {'channel': spisok['channel'],
                              'user': spisok['user'],
                              'message': spisok['message'],
                              'ping': ['предзаказ']}

            else:

                return False, {}
        else:
            return False, {}

    '''def is_live(self):
        twitch_api_stream_url = "https://api.twitch.tv/kraken/streams/" \
                                + self.channels[0] + "?client_id=" + config.Client_id

        streamer_html = requests.get(twitch_api_stream_url)

        streamer = json.loads(streamer_html.content)

        return streamer'''
