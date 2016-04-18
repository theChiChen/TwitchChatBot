# -*- coding: utf-8 -*-
import configparser
import codecs

class Config(object):
    def __init__(self, config_file='config/Options.conf'):
        config = configparser.ConfigParser()
        config.read_file(codecs.open(config_file, "r", "utf-8"))

        self.address = config.get('Server', 'Address', fallback=None)
        self.port = config.getint('Server', 'Port', fallback=None)

        self.nick = config.get('Credentials', 'Nick', fallback=None)
        self.oauth_password = config.get('Credentials', 'Oauth_password', fallback=None)

        self.channel = config.get('Chat', 'Channel', fallback=None)
        self.socket_buffer_size = config.getint('Chat', 'Socket_buffer_size', fallback=1024)
        self.rate = config.getfloat('Chat', 'Rate', fallback=0.67)
        self.broadcast_time = config.getint('Chat', 'Broadcast_time', fallback=300)
        self.welcome_message = config.get('Chat', 'Welcome_message', fallback=None)

        self.debug = config.getboolean('Debug', 'Debug', fallback=True)

        # Validation logic for bot settings.
        if not self.nick or not self.oauth_password:
            raise ValueError('A Nick or Oauth_password was not specified in the configuration file.')