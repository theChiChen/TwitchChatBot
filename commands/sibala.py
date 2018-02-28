# -*- coding: utf-8 -*-

import random

def sibala(args):
	dice = []
	usage = 'sibala usage : !sibala'

	if len(args) == 1:
		for i in range(4):
				dice.append(str(random.randint(1, 6)))
		return args[0] + ' 的點數是 ' + dice[0] + ' ' + dice[1] + ' ' + dice[2] + ' ' + dice[3]
	else:
		return usage