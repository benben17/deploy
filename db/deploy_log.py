# -*- coding: utf-8 -*-

import db
import sys,os
sys.path.append("..")
import ext.module as module

class mf_deploy_log(object):
	"""docstring for mf_deploy_log"""
	def build_log(self,res_info):
		res_info.append(module.YMD())
		self.sql = "insert into build_log (sys_id,env,build_log,build_status,c_t) values(%s,%s,%s,%s,%s)"
		self.values=res_info
		conn=db.db_query()

		re = conn.db_insert(self.sql, self.values)
		if re :
			print "{} : INFO: build log save success".format(module.YMD())
			return True
		else:
			print "{} : ERROR: please found some information from err_log.".format(module.YMD())
			return False
		return True

	def deploy_log(self,res_info):

		res_info.append(module.YMD())

		self.sql = "insert into deploy_log (sys_id,env,deploy_status,c_t) values (%s ,%s,%s,%s)"
		self.values = res_info
		conn=db.db_query()

		re = conn.db_insert(self.sql, self.values)
		if re :
			return True
		else:
			return False
	def conf_log(self,res_info):
		
		res_info.append(module.YMD())

		self.sql = "insert into deploy_log (sys_id,env,type,host_id,deploy_status,c_t) values (%s ,%s,2,%s,%s,%s)"
		self.values = res_info
		conn=db.db_query()

		re = conn.db_insert(self.sql, self.values)
		if re :
			return True
		else:
			return False


if __name__ == '__main__':
	log=mf_deploy_log()
	res=[]
	res=['1','1','1','1']
	print log.build_log(res)

