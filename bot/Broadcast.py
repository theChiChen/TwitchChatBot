# -*- coding: utf-8 -*-
import threading, random, time, select
import Config
import Messages

class Bot(threading.Thread):
	def __init__(self,threadname, interval, socket):
		threading.Thread.__init__(self,name = threadname, daemon = True)
		self.interval = interval
		self.isrunning = True
		self.socket = socket

	def run(self):
		while self.isrunning:
			time.sleep(self.interval)
			readable, writable, exceptional = select.select([], [self.socket], [], 1)
			for sock in writable:
				if sock == self.socket:
					msg = random.choice ( Messages.message )
					self.socket.send(("PRIVMSG #%s :%s\r\n" % (Config.channel, msg)).encode("utf-8"))
					print('[%s][Broadcast] %s' % (time.strftime('%H:%M:%S', time.gmtime()), msg))
		print('[%s][System] %s stop at %s !!' % (time.strftime('%H:%M:%S', time.gmtime()), self.getName(), time.ctime()))

	def stop(self):
		self.isrunning = False