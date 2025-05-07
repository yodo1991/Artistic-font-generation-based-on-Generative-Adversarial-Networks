/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50562
Source Host           : localhost:3306
Source Database       : flaskt

Target Server Type    : MYSQL
Target Server Version : 50562
File Encoding         : 65001

Date: 2025-03-05 23:17:38
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for ai_photo
-- ----------------------------
DROP TABLE IF EXISTS `ai_photo`;
CREATE TABLE `ai_photo` (
  `userid` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `fileanme` varchar(255) DEFAULT NULL,
  `result` varchar(255) DEFAULT NULL,
  `con_level` float(10,0) DEFAULT NULL,
  `login_time` datetime DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of ai_photo
-- ----------------------------
INSERT INTO `ai_photo` VALUES ('admin', 'admin', 'photo_191955518.png', '', '1', '2025-03-05 19:19:55');
INSERT INTO `ai_photo` VALUES ('admin', 'admin', 'photo_192020745.png', '', '2', '2025-03-05 19:20:20');
INSERT INTO `ai_photo` VALUES ('admin', 'admin', 'photo_192024824.png', '', '0', '2025-03-05 19:20:24');
INSERT INTO `ai_photo` VALUES ('admin', 'admin', 'photo_192024860.png', '', '0', '2025-03-05 19:20:24');

-- ----------------------------
-- Table structure for login_logs
-- ----------------------------
DROP TABLE IF EXISTS `login_logs`;
CREATE TABLE `login_logs` (
  `id` int(11) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `username` text NOT NULL,
  `ip_address` text NOT NULL,
  `login_time` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of login_logs
-- ----------------------------
INSERT INTO `login_logs` VALUES ('00000000036', 'admin', '127.0.0.1', '2025-03-05 23:11:00');
INSERT INTO `login_logs` VALUES ('00000000025', 'admin', '127.0.0.1', '2025-02-27 21:30:35');
INSERT INTO `login_logs` VALUES ('00000000026', 'lhf', '127.0.0.1', '2025-03-04 21:42:29');
INSERT INTO `login_logs` VALUES ('00000000027', 'lhf', '127.0.0.1', '2025-03-04 21:47:14');
INSERT INTO `login_logs` VALUES ('00000000028', 'lhf', '127.0.0.1', '2025-03-04 21:47:16');
INSERT INTO `login_logs` VALUES ('00000000029', 'admin', '127.0.0.1', '2025-03-04 22:01:01');
INSERT INTO `login_logs` VALUES ('00000000030', 'admin', '127.0.0.1', '2025-03-04 22:27:58');
INSERT INTO `login_logs` VALUES ('00000000031', 'admin', '127.0.0.1', '2025-03-04 22:49:19');
INSERT INTO `login_logs` VALUES ('00000000032', 'admin', '127.0.0.1', '2025-03-05 19:16:39');
INSERT INTO `login_logs` VALUES ('00000000033', 'admin', '127.0.0.1', '2025-03-05 21:23:54');
INSERT INTO `login_logs` VALUES ('00000000034', 'admin', '127.0.0.1', '2025-03-05 23:08:32');
INSERT INTO `login_logs` VALUES ('00000000035', 'admin', '127.0.0.1', '2025-03-05 23:11:00');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `usertype` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('admin', '123', '管理员');
INSERT INTO `users` VALUES ('user1', '456', '普通用户');
INSERT INTO `users` VALUES ('user2', '789', '普通用户');
INSERT INTO `users` VALUES ('lhf', '1', '普通用户');
