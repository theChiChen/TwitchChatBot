# -*- coding: utf-8 -*-
import threading, random, time, select
import Messages

class Bot(threading.Thread):
	def __init__(self,threadname, socket, config):
		threading.Thread.__init__(self,name = threadname)
		self.isrunning = True
		self.socket = socket
		self.config = config

	def run(self):
		delay = 0
		while self.isrunning:
			time.sleep(1)
			delay = delay + 1
			if delay == self.config.broadcast_time:
				delay = 0
				try:
					readable, writable, exceptional = select.select([], [self.socket], [], 3)
				except select.error:
					self.isrunning = False
					break
				for sock in writable:
					if sock == self.socket:
						msg = random.choice ( Messages.message )
						try:
							self.socket.send(("PRIVMSG #%s :%s\r\n" % (self.config.channel, msg)).encode("utf-8"))
						except socket.error:
							self.isrunning = False
							break
						print('[{}][Broadcast] {}'.format(time.strftime('%H:%M:%S', time.localtime()), msg))
		print('[{}][System] {} stop at {} !!'.format(time.strftime('%H:%M:%S', time.localtime()), self.getName(), time.ctime()))

	def stop(self):
		self.isrunning = False