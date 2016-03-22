# -*- coding: utf-8 -*-

import socket, sys, time, errno, re
import bot.Broadcast as Broadcast
import bot.Chat as Chat
import bot.Login as Login
import Config



if __name__ == '__main__':
	LoginBot = Login.Bot()
	twitch_socket = LoginBot.get_socket()

	BroadcastBot = Broadcast.Bot('BroadcastBot', Config.broadcast_time, twitch_socket)
	ChatBot = Chat.Bot('ChatBot', Config.broadcast_time, twitch_socket)
	BroadcastBot.start()
	ChatBot.start()

	try:
		while BroadcastBot.isAlive() or ChatBot.isAlive():
			pass
	except KeyboardInterrupt:
		BroadcastBot.stop()
		ChatBot.stop()
		print('stopped by keyboard')
