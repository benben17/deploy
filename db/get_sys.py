# -*- coding: utf-8 -*-

import db

class mf_sys():
	"""docstring for mf_sys"""
	def sys_git(self,project_name):
		sql = "select git_addr from sys where project_name='%s'" %(project_name)
		db_conn=db.db_query()
		sys_git = db_conn.db_get_one(sql)
		return sys_git
	def sys_id(self,project_name):
		sql = "select id from sys where project_name='%s'" %(project_name)
		db_conn=db.db_query()
		sys_id = db_conn.db_get_one(sql)
		if sys_id is not None:
			return sys_id
		else:
			return False

	def sys_host(self,project_name,env):
		sql = "select id from sys where project_name='%s'" %(project_name)
		db_conn=db.db_query()
		sys_id = db_conn.db_get_one(sql)
		if sys_id > 0 :
			host_sql="select host_ip,target_dir from hosts where sys_id=%d and env='%s' " %(int(sys_id),env)
			host_ip = db_conn.db_select(host_sql)
			hosts = []
			for ip in host_ip:
				hosts.append(ip)
			# 返回数组格式
			return hosts
		else:
			return None
	def host_conf(self,project_name,env):
		sql = "select id from sys where project_name='%s'" %(project_name)
		db_conn=db.db_query()
		sys_id = db_conn.db_get_one(sql)
		if sys_id > 0 :
			host_sql="select h.id,h.host_ip,CONCAT(h.target_dir,'%s',c.path) path  from hosts h ,sys_conf_file c where c.sys_id=h.sys_id and c.sys_id=%d and h.env='%s'" %('/'+project_name,int(sys_id),env)
			host_ip = db_conn.db_select(host_sql)

			hosts = []
			for ip in host_ip:
				hosts.append(ip)
			# 返回数组格式
			return hosts
		else:
			return None


if __name__ == '__main__':
	de_sys=mf_sys()
	print de_sys.host_conf('appapi','test')
