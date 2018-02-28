# -*- coding: utf-8 -*-

import random, json

def randomemote(args):
	
	usage = 'randomemote usage : !randomemote'
	filename = './commands/global_emotes.json'

	if len(args) == 1:
		try:
			data = json.loads(open(filename, 'r').read())
		except:
			return 'Error reading %s.' % filename 

		emote = random.choice(list(data.keys()))

		return '%s' % (emote)
	else:
		return usage

