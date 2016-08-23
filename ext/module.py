# -*- coding: utf-8 -*-
# version :0.1


import datetime
import ConfigParser
import os,sys

def YMD():
	d=datetime.datetime.now()
	return d.strftime('%Y-%m-%d %H:%M:%S')

#获取config配置文件
def get_config():
    cf 		= ConfigParser.ConfigParser()
    cf_file 	= os.path.split(os.path.realpath(__file__))[0] + '/../conf/deploy.conf'

    if os.path.isfile(cf_file):
    	cf.read(cf_file)
    	return cf
    else:
    	print "can not load config file {}.".format(cf_file)
    	sys.exit(1)


if __name__ == '__main__':
	print get_config().items('log')[0][0]



