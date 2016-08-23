# -*- coding: utf-8 -*-

import db
import os,sys
sys.path.append('..')
import ext.module as module
from ext.log import mf_log 
from get_sys import mf_sys

class sys_conf(object):
	"""docstring for sys_conf_build"""
	def __init__(self):
		self.mf_log = mf_log()

	def conf_file(self,sys_id):
		self.db=db.db_query()
		self.sql="select file_name,id from sys_conf_file where sys_id=%s" % sys_id
		self.res=self.db.db_select(self.sql)
		if len(self.res) > 0:
			return self.res
		else:
			return None

	def conf_var(self,sys_id,env,file_id):
		self.db=db.db_query()
		self.sql="select conf_variable,conf_par from  sys_conf where sys_id=%s and env=%s and file_id=%s order by id" %(sys_id,env,file_id)
		self.res=self.db.db_select(self.sql)
		
		if len(self.res) > 0 :
			return self.res
		else:
			msg = "please confirm {}".format(self.sql)
			self.mf_log.error(msg)
			return None

	def build_file(self,conf):
		# sys_id = conf['sys_id']

		sys_id = mf_sys().sys_id(conf['service'])
		file_path = conf['path']
		env = conf['deploy_env']

		self.cf=self.conf_file(sys_id)
		if self.cf is None:
			msg = 'system can not find any conf file for %s' %(conf['service'])
			self.mf_log.error(msg)
			sys.exit(1)
		#配置文件目录是否存在，不存在 创建目录
		if not os.path.exists(file_path):
			os.makedirs(file_path)

		# 判断是否有文件参数
		# print self.conf_var(sys_id,env,self.cf[0][1])
		if self.conf_var(sys_id,env,self.cf[0][1]) is None:
			msg = 'system con not find any variables file for %s' %(conf['service'])
			self.mf_log.error(msg)
			sys.exit(1)

		if len(self.cf) == 1:
			self.file_name=file_path+"/"+self.cf[0][0]
			msg = "{} {} create conf file success".format(conf['service'],self.file_name)
			self.mf_log.info(msg)
			f=open(self.file_name,'w')
			for var,par in self.conf_var(sys_id,env,self.cf[0][1]):
				try:
					f.write(str(var)+'='+par+'\n')

				except Exception, e:
					print e	
			return True
		# elif len(self.cf)==0:
		# 	print conf['service'],"is not found any conf file.please confirm conf infomation"
		# 	return False

		else:
			for file_name,file_id in self.cf:
				self.file_name=file_path+'/'+file_name
				msg = "{} {} create conf file success".format(conf['service'],self.file_name)
				self.mf_log.info(msg)

				f=open(self.file_name,'w')
				for var,par in self.conf_var(sys_id,env,file_id):
					try:
						f.write(str(var)+'='+par+'\n')
					except Exception, e:
						print e	
						sys.exit(1)
				f.close()

			return True

			

if __name__ == '__main__':
	print "a"