# -*- coding: utf-8 -*-
'''
Deploy for tomcat and dubbo service
'''
import os
import sys
import logging
import commands
import module
sys.path.append('..')
from db.deploy_log import mf_deploy_log as logsave
from db.get_sys import mf_sys  as mf_sys

class mf_deploy():
    """
    Documentation for Deploy,deploy for tomcat and dubbo service
    
    """
    def __init__(self, config):
        self.config = config
        #定义错误日志文件
        self.log_dir = module.get_config().get('log','log_dir')
        self.log_file = self.log_dir +"/"+self.config['service']+".log"

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def deploy(self):

        # 获取需要部署的主机,以及部署目录
        servers = mf_sys().sys_host(self.config['service'],self.config['env'])
        #配置文件package dir 加 服务名  加taget 目录 加服务名.war
        package_file=self.config['package_dir']+self.config['service']+"/target/"+self.config['service']+".war"
        #print self.config
        res_info=[]
        for s,target_dir in servers:
            ansible_par='host=%s path=%s package=%s project_name=%s' % (s,target_dir,package_file,self.config['service'])
            self.cmd='/usr/bin/ansible-playbook '+self.config['yml_file']+' --extra-vars "'+ansible_par+'"'
            print self.cmd
            
            (ret,output) = commands.getstatusoutput(self.cmd)
            # log_file='/tmp/'+self.config['service']+".log"
            if os.path.isfile(self.log_file):
                with open(self.log_file,'a') as f:
                f.write(output)
                f.close()
            else:
                print output
            
            #记录部署日志(系统id，环境，时间，部署状态)
            sys_id = mf_sys().sys_id(self.config['service'])
            res_info=[sys_id,self.config['env']]
            # save_log=mf_log()
	    
            if ret != 0:
                logging.error('{} deploy service error'.format(module.YMD()))
                res_info.append('0')
                logsave().deploy_log(res_info)
                return False
            print  "{} : INFO : deploy {} successful.".format(module.YMD(),s,self.config['service'])
            res_info.append('1')
	    # print res_info
            logsave().deploy_log(res_info)
        return True


    def conf_update(self):
        # 获取需要部署的主机,以及部署目录
        servers = mf_sys().host_conf(self.config['service'],self.config['env'])
        #  需要重新一个
        print servers
        #print self.config
        res_info=[]
        for host_id,s,target_path in servers:
            ansible_par='host=%s path=%s target_path=%s project_name=%s service_type=%s' % (s,self.config['path']+'/*',target_path,self.config['service'],self.config['service_type'])
            self.cmd='/usr/bin/ansible-playbook '+self.config['yml']+' --extra-vars "'+ansible_par+'"'
            print self.cmd

            (ret,output) = commands.getstatusoutput(self.cmd)
            # log_file='/tmp/'+self.config['service']+".log"

            if os.path.isfile(self.log_file):
                with open(self.log_file,'w') as f:
                    f.write(output)
                    f.close()
            else:
                print output

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

    cf=mf_deploy(conf)
    cf.conf_update()
