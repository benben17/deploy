# -*- coding: UTF-8 -*-
# coding: utf-8

import sys

DEPLOY 		="/tmp"
SRC_DIR 	= DEPLOY+"/git/"
PACKING_DIR = DEPLOY+"/packing/"
CONF 		= DEPLOY+"/conf/"


def deploy_env(conf):
	env = None
	if conf['env']	== 'dev':
		env=1
	elif conf['env'] == 'test':
		env=2
	elif conf['env'] == 'stage':
		env=3
	elif conf['env'] == 'online':
		env=4
	elif conf['env'] == 'demo':
		env=5
	else:
		print "can not find env info ,(dev|test|stage|online|demo)"
		sys.exit(1)
	return env


