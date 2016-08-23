# -*- coding: utf-8 -*-

import commands
import sys,os
sys.path.append("..")
import logging
import conf.env  as ENV
from db.deploy_log import mf_deploy_log as logsave
import module
from db.get_sys import mf_sys

class mfpacking():
    """
    get Latest source file for packing
    """
    def __init__(self, config):
        # super(packing, self).__init__(conf)
        self.config = config
        self.git_dir = config['git_dir']+config['service']
        self.packing_dir = config['pack_dir']+config['service']
        #定义错误日志文件 目录不存在则创建目录
        self.log_dir=module.get_config().get('log','log_dir')
        self.log_file = self.log_dir+"/"+self.config['service']+".log"

        if not os.path.exists(self.git_dir):
            os.makedirs(self.git_dir)
        if not os.path.exists(self.packing_dir):
            os.makedirs(self.packing_dir)
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def _checkout(self, repo, path, branch):

        if not os.path.exists(path):
            (ret, out) = commands.getstatusoutput("git clone {} {}".format(
                repo,
                path))
            
            print out
            if ret != 0:
                logging.error("fetch git %s failed",conf['git']['repo'])
                return False
        
        (ret, out) = commands.getstatusoutput("git -C {} pull  && git -C {} checkout {}"
                                              " && git -C {} pull &&"
                                              " git -C {} submodule update --init --recursive &&"
                                              " git -C {} submodule foreach git pull origin master"
                                              .format(path,
                                                  path, branch, path, path, path))

        print out
        if ret != 0:
            logging.error("fetch git %s failed",self.config['git']['repo'])
            return False

        return True
                
    def _fetch(self):
        if not self._checkout(
                self.config['git']['repo'],
                self.git_dir+"/git",
                self.config['git']['branch']):
            return False

        # if not self._checkout(
        #         self.config['conf']['repo'],
        #         self.git_dir + '/conf',
        #         self.config['conf']['branch']):
        #     return False
        
        return True

    def _copy_and_clear(self, source, dest):
        if os.path.exists(dest):
            (ret, out) = commands.getstatusoutput("rm -rf {}".format(dest))
            if ret != 0:
                logging.error("Remove {} failed".format(dest))
                return False
        
        # print source,dest
        (ret, out) = commands.getstatusoutput("cp -rf {} {}".format(
            source, dest))
        if ret != 0:
            logging.error("Copy {} repo failed".format(source))
            return False
        
        (ret, out) = commands.getstatusoutput("rm -rf {}".format(
            dest + '/.git'))
        if ret != 0:
            logging.error("Remove {} .git failed".format(source))
            return False

        return True

    # def _replace(self, source, dest):
    #     for root, dirs, files in os.walk(source, followlinks=True):
    #         for f in files:
    #             f = os.path.join(root, f)
    #             f = f.replace(source, '')
    #             shutil.copyfile(source + f, dest + f)

    #     return False
        
    def _merge(self):
        if not self._copy_and_clear(self.git_dir+'/git',
                                    self.packing_dir):
            return False
        return True

    def get_src(self):
        if not self._fetch():
            logging.error("fetch source failed")
            return False
        if not self._merge():
            logging.error("merge source failed")
            return False
        
        return True
    
    
    def package_now(self,config):
        mvn_cmd=config['mvn_cmd']
        os.chdir(self.packing_dir)
        # print os.getcwd()
        (ret,output) = commands.getstatusoutput(mvn_cmd)

        sys_id = mf_sys().sys_id(config['service'])
        res=[]
        res.append(sys_id)
        res.append(config['deploy_env'])
        res.append(output)
        
        if ret != 0:
            
            # log_file='/tmp/'+self.config['service']+".log"
            with open(self.log_file,'w') as f:
                f.write(output)
                f.close()
            logging.error("maven build failed,please looking for some error from {} log file".format(self.log_file))
            res.append('0')
            logsave().build_log(res)
            return False
            
        res.append('1')
        logsave().build_log(res)
        return True



if __name__ == '__main__':
    conf 					= dict()
    conf['env'] 			= "online"
    conf['git'] 			= dict()
    conf['git_dir'] 	    = "git@10.0.18.4:mftour/appapi.git"
    conf['git']['branch'] 	= "dev"
    conf['pack_dir'] 		= "/tmp/appapi"
    conf['service'] 		= 'appapi'
    # print type(conf)
    pg=mfpacking(conf)
    # # print pg.package_now()

    # print cf.get('log','log_dir')

    # cf = module.get_config()