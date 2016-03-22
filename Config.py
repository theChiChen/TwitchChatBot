# -*- coding: utf-8 -*-

# details required to login to twitch IRC server
server = 'irc.twitch.tv'
port = 6667
nick = 'xxxxx'
oauth_password = 'oauth:xxxxx' # get this from http://twitchapps.com/tmi/

# channel to join
channel = 'xxxxx'
# maximum amount of bytes to receive from socket - 1024-4096 recommended
socket_buffer_size = 1024

# 100 per 30 seconds = Mod   ||||   20 per 30 seconds = User
rate = (20/30)

broadcast_time = 300

welcome_message = 'Hi 大家好!!'

# if set to true will display any data received
debug = False