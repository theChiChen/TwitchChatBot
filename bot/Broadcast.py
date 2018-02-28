# -*- coding: utf-8 -*-
import random, time
import Messages

class Bot():
	def __init__(self, socket, config):
		self.isrunning = True
		self.config = config
		self.socket = socket

	def run(self):
		time.sleep(self.config.broadcast_time)
		while self.isrunning:
			msg = random.choice ( Messages.message )
			self.socket.connection.privmsg(self.socket.channel, msg)
			time.sleep(self.config.broadcast_time)

	def stop(self):
		self.isrunning = False