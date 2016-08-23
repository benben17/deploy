此发布系统分成 3 部分使用：打包，入库，部署。

使用统一的配置，配置为基本不变的数据：
# Main structure has name

## 需要环境
#### 支持python 2.7 不支持 2.6、3.0 以上版本
#### 需要python 模块如下
	- MySQLdb
	- ansible
	- email
	其他还在统计中


## 配置
### 数据库配置

	1 安装MySQL 数据库 ，不要赘述。网上有的是资料
	2 创建数据库  根据自己规则进行创建
	3 数据库初始化，SQL文件在 db目录下 db.sql
	4 创建用户 

### 数据库配置 conf/deploy.conf 后面的值不需要添加引号（' 或者 "）
	[db]
	DB_host	= 123.56.26.112   数据库IP地址
	DB_user	= ***
	DB_pass	= ****
	DB_port = 3306
	db_name = aa
	[log]
	log_dir = /tmp/log    # 定义错误日志目录

	[smtp]
	smtp_host = smtp.exmail.qq.com
	smtp_port = 465
	smtp_user = oprobot@mftour.cn
	smtp_pass = *******
	#域名
	mail_postfix = mftour.cn

### 初始化配置 conf/env.py
	DEPLOY 		="/tmp"      部署目录
	SRC_DIR 		= DEPLOY+"/git/" 源码目录
	PACKING_DIR 	= DEPLOY+"/packing/"  打包目录
	CONF 			= DEPLOY+"/conf/"     配置文件目


错误日志 默认在 /tmp 目录下，文件名称为 ｛service_name｝.log
	


*  打包
	```bash
   python run.py -s service_name[project_name] pack -b BRANCH -e ENV ```

* 打包并目录
	```bash
	python run.py -s service_name[project_name] deploy -e ENV -t [tomcat|dubbo] -b BRANCH```

- 配置文件更新
	```bash
	python run.py -s [service_name|project_name] update -e ENV ```