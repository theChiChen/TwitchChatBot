# -*- coding: utf-8 -*-
import threading, time, select, re
import lib.Command as Command

class Bot(threading.Thread):
	def __init__(self,threadname, socket, config):
		threading.Thread.__init__(self,name = threadname)
		self.isrunning = True
		self.socket = socket
		self.config = config

	def receive_chat_data(self):
		try:
			readable, writable, exceptional = select.select([self.socket], [], [], 1)
		except select.error:
			self.isrunning = False
			return None
		for sock in readable:
			if sock == self.socket:
				try:
					socket_data = self.socket.recv(self.config.socket_buffer_size).decode("utf-8", "ignore")
				except socket.error:
					self.isrunning = False
					return None
				if len(socket_data) == 0:
					print('[%s][#%s][Error] Connection was lost.' % (time.strftime('%H:%M:%S', time.localtime()), self.config.channel))
					self.isrunning = False
					return None
				if socket_data == "PING :tmi.twitch.tv\r\n":
					self.sendPONG()
					print("PONG")
					return None
				else:
					socket_data = socket_data.rstrip("\r\n")
				return socket_data
		return None

	def getMessage(self, data):
		separate = data.split(":", 2)
		user = separate[1].split("!", 1)[0]
		message = separate[2]
		return user, message, re.findall(r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :', data)[0]

	def sendMessage(self, msg):
		self.socket.send(("PRIVMSG #%s :%s\r\n" % (self.config.channel, msg)).encode("utf-8"))
		print("[%s][#%s][Chat] !*me : %s" % (time.strftime('%H:%M:%S', time.localtime()), self.config.channel, msg))

	def sendPONG(self):
		self.socket.send(("PONG :tmi.twitch.tv\r\n").encode("utf-8"))

	def stop(self):
		self.isrunning = False

	def run(self):
		Commandlib = Command.Commandlib()
		while self.isrunning:
			chat_data = self.receive_chat_data()
			if chat_data is not None:
				user, msg, channel = self.getMessage(chat_data)
				if self.config.debug:
					print(chat_data)
				try:
					print("[%s][%s][Chat] %s : %s" % (time.strftime('%H:%M:%S', time.localtime()), channel, user, msg))
				except:
					print("[%s][%s][Error] %s : I can't encode character!!" % (time.strftime('%H:%M:%S', time.localtime()), channel, self.getName()))
				if Commandlib.is_valid_command(msg) or Commandlib.is_valid_command(msg.split(' ')[0]):
					if Commandlib.check_returns_function(msg.split(' ')[0]):
						if Commandlib.check_has_correct_args(msg, msg.split(' ')[0]):
							args = msg.split(' ')
							args[0] = user
							command = msg.split(' ')[0]
							msg_p = Commandlib.pass_to_function(msg.split(' ')[0], args)
							if msg_p:
								self.sendMessage(msg_p)
					else:
						if Commandlib.check_has_return(msg):
							msg_p = Commandlib.get_return(msg)
							self.sendMessage(msg_p)
				time.sleep(1/self.config.rate)
		print('[%s][System] %s stop at %s !!' % (time.strftime('%H:%M:%S', time.localtime()), self.getName(), time.ctime()))