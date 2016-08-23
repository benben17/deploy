DROP TABLE IF EXISTS `build_log`;
CREATE TABLE `build_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sys_id` int(11) NOT NULL DEFAULT '0' COMMENT '系统ID',
  `env` tinyint(4) NOT NULL DEFAULT '0' COMMENT '1:dev 2:test 3:stage 4:online 5:demo',
  `build_log` varchar(60000) NOT NULL DEFAULT '',
  `build_status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '1:success 2:failed',
  `c_t` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `sys_id` (`sys_id`)
) ENGINE=Innodb AUTO_INCREMENT=79 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `deploy_log`
-- ----------------------------
DROP TABLE IF EXISTS `deploy_log`;
CREATE TABLE `deploy_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `env` varchar(36) NOT NULL,
  `sys_id` int(11) NOT NULL DEFAULT '0' COMMENT '系统ID',
  `c_t` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `deploy_status` tinyint(4) NOT NULL COMMENT '0 failed 1 success',
  PRIMARY KEY (`id`),
  KEY `sys_id` (`sys_id`)
) ENGINE=Innodb AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hosts`
-- ----------------------------
DROP TABLE IF EXISTS `hosts`;
CREATE TABLE `hosts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sys_id` int(11) NOT NULL DEFAULT '0' COMMENT '系统ID',
  `host_ip` varchar(32) NOT NULL DEFAULT '' COMMENT 'host IP',
  `host_port` int(11) NOT NULL DEFAULT '0' COMMENT 'host port',
  `target_dir` varchar(128) NOT NULL DEFAULT '' COMMENT '部署目录',
  `service_port` smallint(6) NOT NULL DEFAULT '0' COMMENT 'service port',
  `env` varchar(24) NOT NULL COMMENT 'deploy env',
  PRIMARY KEY (`id`),
  KEY `sys_id` (`sys_id`),
  KEY `host_ip` (`host_ip`)
) ENGINE=Innodb AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `sys`
-- ----------------------------
DROP TABLE IF EXISTS `sys`;
CREATE TABLE `sys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sys_name` varchar(32) NOT NULL DEFAULT '' COMMENT '系统名称',
  `project_name` varchar(32) NOT NULL DEFAULT '' COMMENT '工程名',
  `git_addr` varchar(128) NOT NULL DEFAULT '' COMMENT 'GIT 地址',
  `sys_owner` varchar(16) NOT NULL DEFAULT '' COMMENT '系统负责人',
  `c_t` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `sys_name` (`sys_name`)
) ENGINE=Innodb AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `sys_conf`
-- ----------------------------
DROP TABLE IF EXISTS `sys_conf`;
CREATE TABLE `sys_conf` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `env` tinyint(4) NOT NULL DEFAULT '0' COMMENT '1:dev 2:test 3:stage 4:online 5:demo',
  `sys_id` int(11) NOT NULL DEFAULT '0' COMMENT 'system id ',
  `file_id` int(11) NOT NULL COMMENT 'confile file id',
  `conf_variable` varchar(64) NOT NULL DEFAULT '' COMMENT '变量',
  `conf_par` varchar(1000) NOT NULL DEFAULT '' COMMENT '参数',
  `is_enable` tinyint(4) NOT NULL DEFAULT '1' COMMENT '1:enabled,0:disable',
  `c_t` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `env` (`env`,`sys_id`,`file_id`,`conf_variable`),
  KEY `sys_id` (`sys_id`)
) ENGINE=Innodb AUTO_INCREMENT=45 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `sys_conf_file`
-- ----------------------------
DROP TABLE IF EXISTS `sys_conf_file`;
CREATE TABLE `sys_conf_file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sys_id` int(11) NOT NULL DEFAULT '0' COMMENT '系统ID',
  `file_name` varchar(32) NOT NULL DEFAULT '' COMMENT '配置文件名称',
  `c_t` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `sys_id` (`sys_id`,`file_name`)
) ENGINE=Innodb AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
