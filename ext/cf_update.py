#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version :0.1
# author : benben
import sys,os
import module
import commands
sys.path.append('..')
from db.deploy_log import mf_deploy_log as logsave
from db.get_sys import mf_sys  as mf_sys

class cf_update():
	"""docstring for config file update"""
	def __init__(self,config):
		self.config = config
		#定义错误日志文件
		self.log_dir = module.get_config().get('log','log_dir')
		self.log_file = self.log_dir +"/"+self.config['service']+".log"

		if not os.path.exists(self.log_dir):
			os.makedirs(self.log_dir)

	def conf_update(self):
		# 获取需要部署的主机,以及部署目录
		servers = mf_sys().host_conf(self.config['service'],self.config['env'])
		#  需要重新一个
		print servers
		#print self.config
		res_info=[]
		for host_id,s,target_path in servers:
			ansible_par='host=%s path=%s target_path=%s project_name=%s' % (s,self.config['path'],target_path,self.config['service'])
			self.cmd='/usr/bin/ansible-playbook '+self.config['yml']+' --extra-vars "'+ansible_par+'"'
			print self.cmd

			(ret,output) = commands.getstatusoutput(self.cmd)
            # log_file='/tmp/'+self.config['service']+".log"
			with open(self.log_file,'w') as f:
				f.write(output)
				f.close()
			print host_id
			#记录部署日志(系统id，环境，时间，部署状态)
			sys_id = mf_sys().sys_id(self.config['service'])
			res_info=[sys_id,self.config['env'],host_id]
			# save_log=logsave()

			if ret != 0:
				print '{} : ERROR : deploy service error.'.format(module.YMD())
				res_info.append('0')
				logsave().conf_log(res_info)
				return False

			print  "{} : INFO : deploy {} successful.".format(module.YMD(),s,self.config['service'])
			res_info.append('1')
			print res_info
			logsave().conf_log(res_info)
		return True


if __name__ == '__main__':
	conf = dict()
	conf['path'] = '/tmp/config/'
	conf['service'] = 'appapi'
	conf['target_path'] = '/data/webapps/'+conf['service']
	conf['env'] = 'test'
	conf['yml'] = '../cong/cf_update.yml'

	cf_up=cf_update(conf)
	cf_up.conf_update()

