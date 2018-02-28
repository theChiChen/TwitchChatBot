# -*- coding: utf-8 -*-
import time
import irc.bot
import requests
import lib.Command as Command
from lib.Config import Config

import _thread
import bot.Broadcast as Broadcast

import logging, datetime

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, config):
        self.client_id = config.client_id
        self.token = config.oauth_password
        self.channel = '#' + config.channel
        self.debug = config.debug

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + config.channel
        headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        TwitchBotLogger.info("Connecting to {} on port {} ...".format(config.address, str(config.port)))
        irc.bot.SingleServerIRCBot.__init__(self, [(config.address, config.port, 'oauth:'+self.token)], config.nick, config.nick)

    def on_welcome(self, c, e):
        TwitchBotLogger.info("Joining {}".format(self.channel))
        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

        # Make thread for broadcast bot
        _thread.start_new_thread(Broadcast.Bot(self, config).run, ())

    def on_pubmsg(self, c, e):
        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            arguments = e.arguments[0].split(' ')
            arguments[0] = e.source.nick
            TwitchBotLogger.info("Get [{}] {} : {}".format(self.channel, e.source.nick, cmd))
            self.do_command(e, cmd.lower(), arguments)
        return

    def do_command(self, e, cmd, arguments):
        c = self.connection
        
        # Poll the API to get current game.
        if cmd == "game":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' is currently playing ' + r['game'])

        # Poll the API the get the current status of the stream
        elif cmd == "title":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' channel title is currently ' + r['status'])

        else:
            Commandlib = Command.Commandlib()
            if Commandlib.is_valid_command(cmd):
                if Commandlib.check_returns_function(cmd):
#                    if Commandlib.check_has_correct_args(cmd, arguments):
                    message = Commandlib.pass_to_function(cmd, arguments)
                    if message:
                        c.privmsg(self.channel, message)
                        TwitchBotLogger.info("To " + arguments[0] + " Message : " + message)
                else:
                    if Commandlib.check_has_return(cmd):
                        message = Commandlib.get_return(cmd)
                        c.privmsg(self.channel, message)
                        TwitchBotLogger.info("To " + arguments[0] + " Message : " + message)
            else:
                c.privmsg(self.channel, "Hey " + arguments[0] + " , I do not understand your command : " + cmd)
                TwitchBotLogger.info("Hey " + arguments[0] + " , I do not understand your command : " + cmd)

if __name__ == "__main__":
    try:
        config = Config()
        # 基礎設定
        log_filename = datetime.datetime.now().strftime("log/%Y-%m-%d_%H_%M_%S.log")
        logging.basicConfig(level=config.debug,
                            format='%(asctime)s %(name)-25s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            handlers = [logging.FileHandler(log_filename, 'w', 'utf-8'),])
        # 定義 handler 輸出 sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        # 設定輸出格式
        formatter = logging.Formatter('%(name)-25s: %(levelname)-8s %(message)s')
        # handler 設定輸出格式
        console.setFormatter(formatter)
        # 加入 hander 到 root logger
        logging.getLogger('').addHandler(console)

        TwitchBotLogger = logging.getLogger('TwitchBot')

        bot = TwitchBot(config)
        bot.start()
    except KeyboardInterrupt:
        print('Stopped by keyboard')    