#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version :0.1
# author : benben

import sys
import os
import conf.env as ENV
from db.get_conf import sys_conf as conf_build
from ext.package import mfpacking as mf_package
import  argparse
import ext.module as module
from ext.deploy import mf_deploy
from ext.log  import mf_log as log
from db.get_sys import mf_sys


parser = argparse.ArgumentParser(description="Wrapper for deploy commands")
parser.add_argument('-s', help="Service name", required=True)
subparsers = parser.add_subparsers(help="sub-command help")

p_parser = subparsers.add_parser('pack', help="Package the project")
p_parser.add_argument('-b', help="repo branch", required=True)
p_parser.add_argument('-e', help="package environment", required=True)
p_parser.set_defaults(which="pack")

d_parser = subparsers.add_parser('deploy', help="Deploy the project")
d_parser.add_argument('-b', help="repo branch", required=True)
d_parser.add_argument('-e', help="package environment", required=True)
d_parser.add_argument('-t', help="Deploy service Type tomcat or dubbo ", required=True)
d_parser.set_defaults(which="deploy")

d_parser = subparsers.add_parser('update', help="Update config file for project")
d_parser.add_argument('-e', help="package environment", required=True)
d_parser.set_defaults(which="update")


def packing_now(env,service,git_branch):

    conf 					= dict()
    conf['env'] 			= env
    conf['git'] 			= dict()
    conf['git']['repo'] 	= mf_sys().sys_git(service)
    conf['git']['branch'] 	= git_branch
    conf['git_dir'] 		= ENV.SRC_DIR
    conf['pack_dir']        = ENV.PACKING_DIR
    conf['service'] 		= service
    # conf['sys_id']          = sys_id
    conf['path']            = ENV.CONF+conf['service']+"/"+conf['env']   # 根据不同的环境创建对应环境的目录
    conf['deploy_env']      = ENV.deploy_env(conf)
    conf['mvn_cmd']         = "mvn clean package -P{} -am -Dmaven.test.skip".format(conf['env'])

    #生成对应环境的配置文件
    mf_sys_conf = conf_build()
    if mf_sys_conf.build_file(conf) :
        log().info('Build conf file success')
    else:
        print log().error('Build conf file failed,please find some information from logfile')
        return None

    mf_pg = mf_package(conf)
    #获取最新的源码
    if mf_pg.get_src() is True:
        log().info("git checkout success %s" %(conf['git']['repo']))
    else:
        log().error("checkout failed,please find some information from logfile")
        return False
    # 封装成war包
    if mf_pg.package_now(conf) is not True:
        log().error("send email to {}  owner".format(conf['service']))
        return False
    else:
        log().info("{} package successful".format(module.YMD(),conf['service']))
    return True
def deploy_tomcat(env,service):
    ''' 定义部署Tomcat 服务 '''
    conf            = dict()
    conf['env']     = env
    conf['service'] = service
    conf['yml_file']= sys.path[0] +  '/conf/deploy_tomcat.yml'
    conf['service_type'] = "tomcat"
    conf['package_dir']=ENV.PACKING_DIR
    deploy = mf_deploy(conf)
    ret = deploy.deploy()
    print ret 
    print conf
    if not ret:
        log().error(" Deploying {} failed.".format(conf['service']))
    else:
        log().info(" Deploying {} successful.".format(module.YMD(),conf['service']))

def deploy_dubbo(env,service):
    conf                = dict()
    conf['env']         = env
    conf['service']     = service

def conf_update(service,env,service_type):
    conf                = dict()
    conf['env']         = env
    conf['path']        = ENV.CONF+service+"/"+env
    conf['service']     = service
    conf['deploy_env']  = ENV.deploy_env(conf)
    conf['yml']         = sys.path[0] +  '/conf/cf_update.yml'
    conf['service_type']= service_type
    #生成 最新的配置文件
    mf_sys_conf = conf_build()
    if mf_sys_conf.build_file(conf) :
        log().info('Build conf file success')
    else:
        print log().error('Build conf file failed,please find some information from logfile')
        return None

    #配置更新到主机
    deploy = mf_deploy(conf)
    ret = deploy.conf_update()
    if not ret:
        log().error(" config file  {} update failed.".format(conf['service']))
    else:
        log().info(" config file  {} update successful.".format(module.YMD(),conf['service']))


if __name__ == '__main__':

    # ret = packing_now('test','appapi','release')
    conf_update('appapi','test')
    args = parser.parse_args()  #获取参数
    if args.which == 'pack':
        ret = packing_now(args.e,args.s,args.b)
        if ret is None:
            sys.exit(1)
   
    if args.which == 'deploy':
        ret = packing_now(args.e,
                        args.s,
                        args.b)
        if ret is None:
            sys.exit(1)
  	
        if args.t == 'tomcat':
            ret = deploy_tomcat(args.e,
				                args.s)
            if ret is None:
                sys.exit(1)
        if args.t == 'dubbo':
            ret = deploy_dubbo(args.e,
                                args.s)
            if ret is None:
                sys.exit(1)
    if args.which == 'update':
        ret = conf_update(args.s,args.e,args.t)
        if ret is None:
            sys.exit(1)

