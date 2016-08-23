#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version :0.1
# author : benben

import MySQLdb
import sys
sys.path.append('..')
import ext.module as module


class db_query():
	"""docstring for db_query"""
	#DB_host,DB_user,DB_pass,DB_port,db_name
	def __init__(self):
		db_cf 			= module.get_config()
		self.DB_host	= db_cf.get('db', 'DB_host')
		self.DB_user	= db_cf.get('db', 'DB_user')
		self.DB_pass	= db_cf.get('db', 'DB_pass')
		self.DB_port   	= db_cf.getint('db', 'DB_port')
		self.db_name 	= db_cf.get('db', 'db_name')
		
	def db_conn(self):
		try:
			conn=MySQLdb.connect(host=self.DB_host,user=self.DB_user,passwd=self.DB_pass,port=self.DB_port,connect_timeout=5)
			return conn
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			return None
		# finally:
		# 	print "Coun't connect %s:%s" %(self.DB_host,self.DB_port)
		# 	
	
	def db_insert(self,sql,sql_values):
		self.conn = self.db_conn()
		if self.conn is None:
			sys.exit(1)
		self.conn.select_db(self.db_name)
		self.cur = self.conn.cursor()
		try:
			self.cur.execute(sql,sql_values)
		except MySQLdb.Error, e:  
			print "Error %d: %s" % (e.args[0], e.args[1])
		
		self.conn.commit()
		self.cur.close()
		self.conn.close()
		return True
		
	def db_select(self,sql):
		self.conn = self.db_conn()
		if self.conn is None:
			sys.exit(1)
		self.conn.select_db(self.db_name)
		self.cur = self.conn.cursor()
		try:
			self.cur.execute(sql)
		except Exception, e:
			print e,sql		
		self.re = self.cur.fetchall();
		self.cur.close()
		self.conn.close()
		if self.re is not None:
			return self.re
		else:
			return False


	def db_get_one(self,sql):
		self.conn = self.db_conn()
		if self.conn is None:
			sys.exit(1)
		self.conn.select_db(self.db_name)
		self.cur = self.conn.cursor()
		self.cur.execute(sql)
		self.re = self.cur.fetchone()
		self.cur.close()
		self.conn.close()

		if self.re is not  None:
			return self.re[0]
		else:
			return None

if __name__ == '__main__':
	db=db_query()
	db.db_conn()

# 	db=db_query('123.56.26.112', 'deploy', 'deploymftour@!', 3306, "aa")
# 	db.db_conn()
# # 	re=db.db_select("select host_ip,webapp_dir,service_port from hosts")
# # 	for row in re:
# # 		print row[0],row[1]
# # 	# sql="insert into hosts (sys_id,host_ip,host_port,webapp_dir,service_port) values(%s,%s,%s,%s,%s)"
# # 	# sql_values=[1,'10.10.30.4',50022,'/data/webapps',8018]
# # 	# db_add=db.db_insert(sql, sql_values)
# # 	# if db_add is True:
# # 	# 	print "add success"

