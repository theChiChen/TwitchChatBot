# -*- coding: utf-8 -*-
import socket, sys, time, errno, re
import bot.Broadcast as Broadcast
import bot.Chat as Chat
import bot.Login as Login
from lib.Config import Config

if __name__ == '__main__':
	loop = True
	config = Config()
	while loop:
		LoginBot = Login.Bot(config)
		twitch_socket = LoginBot.get_socket()

		BroadcastBot = Broadcast.Bot('BroadcastBot', twitch_socket, config)
		ChatBot = Chat.Bot('ChatBot', twitch_socket, config)
		BroadcastBot.start()
		ChatBot.start()

		try:
			while BroadcastBot.isAlive() and ChatBot.isAlive():
				pass
			if not ChatBot.isAlive():
				if BroadcastBot.isAlive():
					BroadcastBot.stop()
			elif not BroadcastBot.isAlive():
				if ChatBot.isAlive():
					ChatBot.stop()
			time.sleep(5)	
		except KeyboardInterrupt:
			BroadcastBot.stop()
			ChatBot.stop()
			loop = False
			print('stopped by keyboard')
