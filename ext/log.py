#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version :0.1
# author : benben
import sys
import os
import module as module

class mf_log():
	"""docstring for log"""
	def __init__ (self):
		self.date = module.YMD()

	def info(self,msg):
		self.level= sys._getframe().f_code.co_name.upper()
		print "{} : {} : {}".format(self.date,self.level,msg)
	def war(self,msg):
		self.level= sys._getframe().f_code.co_name.upper()
		print " {} : {} : {}".format(module.YMD(),
									self.level,
									msg)
	def error(self,msg):
		self.level= sys._getframe().f_code.co_name.upper()
		print " {} : {} : {}".format(module.YMD(),
									self.level,
									msg)
		# sys.exit(1)

if __name__ == '__main__':

	mf_log=mf_log()
	mf_log.info('aaaa')
