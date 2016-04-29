-- MySQL dump 10.13  Distrib 5.6.27, for Linux (x86_64)
--
-- Host: localhost    Database: main
-- ------------------------------------------------------
-- Server version	5.6.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activity`
--

DROP TABLE IF EXISTS `activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `desc` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity`
--

LOCK TABLES `activity` WRITE;
/*!40000 ALTER TABLE `activity` DISABLE KEYS */;
INSERT INTO `activity` VALUES (1,'限时美折','上线打折','2015-11-30 21:00:00','2015-12-10 00:00:00','2015-11-30 21:56:31');
/*!40000 ALTER TABLE `activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activity_item`
--

DROP TABLE IF EXISTS `activity_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `activity_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `activity_id` int(11) DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `sort_order` int(11) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `image` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `activity_id` (`activity_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `activity_item_ibfk_1` FOREIGN KEY (`activity_id`) REFERENCES `activity` (`id`),
  CONSTRAINT `activity_item_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_item`
--

LOCK TABLES `activity_item` WRITE;
/*!40000 ALTER TABLE `activity_item` DISABLE KEYS */;
INSERT INTO `activity_item` VALUES (1,1,16,10,880.00,'subcaticon/1448941213.95'),(2,1,7,1,880.00,'subcaticon/1448941231.99'),(3,1,6,2,300.00,'subcaticon/1448941251.18');
/*!40000 ALTER TABLE `activity_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_user`
--

DROP TABLE IF EXISTS `admin_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `passwd` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_user`
--

LOCK TABLES `admin_user` WRITE;
/*!40000 ALTER TABLE `admin_user` DISABLE KEYS */;
INSERT INTO `admin_user` VALUES (1,'xianpeng','123456','2015-11-30 10:32:05');
/*!40000 ALTER TABLE `admin_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('314740bf50b9');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `city_code` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `city_code` (`city_code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city`
--

LOCK TABLES `city` WRITE;
/*!40000 ALTER TABLE `city` DISABLE KEYS */;
INSERT INTO `city` VALUES (1,'上海','289');
/*!40000 ALTER TABLE `city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coupon`
--

DROP TABLE IF EXISTS `coupon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coupon` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `price` decimal(10,2) NOT NULL,
  `cat` tinyint(1) NOT NULL,
  `effective` int(11) NOT NULL,
  `remark` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coupon`
--

LOCK TABLES `coupon` WRITE;
/*!40000 ALTER TABLE `coupon` DISABLE KEYS */;
INSERT INTO `coupon` VALUES (1,100.00,0,2592000,'');
/*!40000 ALTER TABLE `coupon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `credit_apply`
--

DROP TABLE IF EXISTS `credit_apply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `credit_apply` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_no` varchar(18) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `school` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `enrollment_time` datetime DEFAULT NULL,
  `major` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `stu_no` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `stu_years` int(11) DEFAULT NULL,
  `addr` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `parent_contact` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `chsi_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `chsi_passwd` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_card_photo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `stu_card_photo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `reason` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `graduate_time` datetime DEFAULT NULL,
  `stu_education` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `credit_apply_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credit_apply`
--

LOCK TABLES `credit_apply` WRITE;
/*!40000 ALTER TABLE `credit_apply` DISABLE KEYS */;
INSERT INTO `credit_apply` VALUES (2,1,'哈哈','421245566776656667','挺有','2015-12-01 00:00:00','哈哈哈','规划好',4,'有意义','1555','哥哥哥哥','蝇营狗苟','apply/1449039530.85','apply/1449039543.61','2015-12-02 12:03:14','2015-12-02 14:59:08',2,'111','2015-12-01 00:00:00','本科'),(3,2,'王前发','450566778755466787','大大方方','2015-12-01 00:00:00','vghh 很好','给刚刚好',4,'哥哥哥哥','5662896','哥哥哥哥','高规格','apply/1449027304.83','apply/1449027309.75','2015-11-30 16:22:23','2015-12-02 11:35:32',3,'回家看看','2016-07-01 00:00:00','本科'),(4,4,'托马斯','340826199612130313','北大','2013-11-01 00:00:00','信息技术','38',4,'天南门','13122022388','1438458','123456','apply/1448889079.31','apply/1448889082.19','2015-11-30 21:11:04','2015-11-30 21:12:26',3,NULL,'2017-11-01 00:00:00','专科');
/*!40000 ALTER TABLE `credit_apply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `credit_change_log`
--

DROP TABLE IF EXISTS `credit_change_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `credit_change_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `credit_change_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credit_change_log`
--

LOCK TABLES `credit_change_log` WRITE;
/*!40000 ALTER TABLE `credit_change_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `credit_change_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `credit_use_log`
--

DROP TABLE IF EXISTS `credit_use_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `credit_use_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `credit_use_log_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`),
  CONSTRAINT `credit_use_log_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credit_use_log`
--

LOCK TABLES `credit_use_log` WRITE;
/*!40000 ALTER TABLE `credit_use_log` DISABLE KEYS */;
INSERT INTO `credit_use_log` VALUES (1,2,6000.00,NULL,'2015-11-30 16:22:59',2),(2,2,4000.00,NULL,'2015-11-30 16:27:17',1),(3,1,1000.00,NULL,'2015-11-30 16:29:32',1),(4,1,5179.40,NULL,'2015-11-30 20:05:16',1),(5,1,-5179.40,NULL,'2015-11-30 22:09:13',1),(6,1,8137.00,NULL,'2015-12-01 14:42:46',1),(7,2,597.40,NULL,'2015-12-01 17:43:59',1),(8,2,-597.40,NULL,'2015-12-01 17:44:16',1);
/*!40000 ALTER TABLE `credit_use_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `edit_name_log`
--

DROP TABLE IF EXISTS `edit_name_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `edit_name_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `edit_name_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `edit_name_log`
--

LOCK TABLES `edit_name_log` WRITE;
/*!40000 ALTER TABLE `edit_name_log` DISABLE KEYS */;
INSERT INTO `edit_name_log` VALUES (1,1,'2015-11-30 11:19:40'),(2,4,'2015-11-30 16:46:13'),(4,2,'2015-11-30 21:37:12'),(5,13,'2015-11-30 21:41:47'),(6,7,'2015-12-01 15:01:45');
/*!40000 ALTER TABLE `edit_name_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `help_cat`
--

DROP TABLE IF EXISTS `help_cat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `help_cat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `help_cat`
--

LOCK TABLES `help_cat` WRITE;
/*!40000 ALTER TABLE `help_cat` DISABLE KEYS */;
INSERT INTO `help_cat` VALUES (1,'分期问题'),(3,'售后服务'),(2,'账单还款');
/*!40000 ALTER TABLE `help_cat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `help_entry`
--

DROP TABLE IF EXISTS `help_entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `help_entry` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cat_id` int(11) DEFAULT NULL,
  `content` varchar(10000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cat_id` (`cat_id`),
  CONSTRAINT `help_entry_ibfk_1` FOREIGN KEY (`cat_id`) REFERENCES `help_cat` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `help_entry`
--

LOCK TABLES `help_entry` WRITE;
/*!40000 ALTER TABLE `help_entry` DISABLE KEYS */;
INSERT INTO `help_entry` VALUES (55,'哪些人能分期',1,'美分分的分期目前仅限全国正规统招全日制在校研究生、本科以及专科的学生。'),(56,'最多能分几期？',1,'您可选的最多分期期数取决于您的毕业时间，您需要在毕业前六个月将最后一期还清，如下:\n<style>\n    table {\n        width: 100%;\n        border: 0;\n        text-align: center;\n    }\n</style>\n<table border=\"1\">\n<tr>\n  <th>学制</th>\n  <td>年级</td>\n  <td>最多分期数</td>\n</tr>\n\n<tr>\n  <th rowspan=\"3\">大专（三年制）</th>\n  <td>专一</td>\n  <td>24期</td>\n</tr>\n<tr>\n  <td>专二</td>\n  <td>16期</td>\n</tr>\n<tr>\n  <td>专三</td>\n  <td>4期</td>\n</tr>\n\n<tr>\n  <th rowspan=\"4\">本科（四年制）</th>\n  <td>大一</td>\n  <td>24期</td>\n</tr>\n<tr>\n  <td>大二</td>\n  <td>24期</td>\n</tr>\n<tr>\n  <td>大三</td>\n  <td>16期</td>\n</tr>\n<tr>\n  <td>大四</td>\n  <td>4期</td>\n</tr>\n\n<tr>\n  <th rowspan=\"2\">研究生（两年制）</th>\n  <td>研一</td>\n  <td>16期</td>\n</tr>\n<tr>\n  <td>研二</td>\n  <td>4期</td>\n</tr>\n\n<tr>\n  <th rowspan=\"3\">研究生（三年制）</th>\n  <td>研一</td>\n  <td>24期</td>\n</tr>\n<tr>\n  <td>研二</td>\n  <td>16期</td>\n</tr>\n<tr>\n  <td>研三</td>\n  <td>4期</td>\n</tr>\n\n\n</table>'),(57,'如何分期下单',1,'1、通过美分分微信公众号找到你想要的项目\n2、选择你的分期计划，然后点击［立即购买］进入到提交订单页面\n3、如还未申请消费额度需要先［申请额度］，提交相关申请信息资料\n4、确认订单以及分期金额，如项目总价超过预计额度6000元，需首付超出部分\n5、提交支付订单即可分期下单成功'),(58,'申请额度需要哪些资料',1,'1、填写基础信息（姓名、身份证号、学校校区、入学时间、学历、专业、学号、宿舍详细地址、学信网账号、学信网密码、父或母联系号码）\n2、上传手持证件照片（手持身份证照片、手持学生证照片）'),(59,'额度不够怎么办',1,'当额度不够时，需要你首付超出部分（项目总价－你的额度）'),(60,'下单成功后如何前往服务',1,'1、打电话到医院进行预约，确认手术时间。注意：预约不需要提供服务码，只需要提供手机号、姓名即可\n2、按照预约时间前往医院，通过服务码、身份证验证后，即可进行手术'),(61,'为什么会额度申请失败',1,'如果出现额度申请失败，有可能是以下原因：\n1、填写的基础信息错误或不真实\n2、上传的手持证件照片不清晰\n3、提交的资料和学信网不一致'),(62,'额度还会提高吗',1,'会的，美分分会根据你的信息资料和账单还款情况，适时为你调高消费额度'),(63,'什么时候需要还款',2,'在你手术完成后即生成账单，并记录在下期账单里，你将有至少30天的时间然后开始还款，每期账单还款截止时间为次月1日'),(64,'如何还款',2,'你可以通过微信支付进行还款'),(65,'可以一次性多还吗',2,'可以的，你可以在我要还款里分别对账单进行还款'),(66,'账单逾期会怎样',2,'如在还款日前未及时清还应还账单，将产生滞纳金，每日滞纳金为当月应还金额的1%，同时逾期记录会记录在您的信用记录中，建议及时还款，珍惜个人信用'),(67,'拒绝还款会怎样',2,'如果您存在恶意拖欠行为，将会对您的信用记录产生负面影响，这将直接影响您未来购房购车和一切与信用有关的行为。同时，我们也会保留根据授信合同采取司法手段追回逾期款项的权利。'),(68,'如何取消订单',3,'未预约订单您可以在个人－我的订单里找到相应订单进行取消操作'),(69,'取消订单需要费用吗',3,'未手术订单取消是不需要费用的，取消后会及时恢复您的额度，如有首付款项也会原路返还'),(70,'取消订单后首付怎么办',3,'如取消订单，首付款项会原路返还'),(71,'预约后可以取消订单吗？',3,'已成功预约的订单，如想取消，需先打电话给医院取消预约，后方可操作取消订单'),(72,'手术完成后有问题怎么办',3,'如手术完成后出现问题或异议，你都可以拨打我们的客服电话进行反馈核实，我们将协助你共同和医院协商解决');
/*!40000 ALTER TABLE `help_entry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hospital`
--

DROP TABLE IF EXISTS `hospital`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hospital` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tags` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `addr` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `long_lat` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `desc` varchar(10000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `working_time` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `photos` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `city_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `city_id` (`city_id`),
  CONSTRAINT `hospital_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `city` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hospital`
--

LOCK TABLES `hospital` WRITE;
/*!40000 ALTER TABLE `hospital` DISABLE KEYS */;
INSERT INTO `hospital` VALUES (1,'上海美未央医疗美容整形医院','4006177321','民营美容医院, 上市集团直投, 国内外专家汇聚','上海市徐汇区漕宝路111号','121.424442,31.167829','千年传承 续写美丽传奇\r\n千年前的盛世汉唐，未央宫的美人们以黛画眉，蘸丹沙点绛唇，引领古代美容潮流。千年后的美未央，传承传统汉唐美学理念，结合现代医学手段，汇聚中、韩、日、台湾等地整形美容大家，运用国际水平的专业技术与顶级医疗美容服务为高标准的求美者提供专业化、国际化、个性化的系列专属整形美容与健康综合解决方案，续写千年的美丽传奇。\r\n上市公司直接投资 明星达人首选医院\r\n上海美未央医疗美容医院坐落于上海市徐汇区漕宝路111号，是由上市公司参与投资的全新理念整形美容医院，明星及时尚人士首选医院。美未央下辖整形美容外科、美容皮肤科、美容口腔科三个核心临床科室，为广大求美者提供涵盖整形美容、激光美肤、皮肤养护、注射美容、牙美容和抗衰老、功能医学、境外医疗等全系列医美服务。\r\n高品质个性化服务 专注医疗技术效果\r\n医院汇聚中、韩、法、日、台湾等地整形美容大家，拥有实力强大的国际级医疗专家团队，国内外最新技术及仪器设备，致力于将中国传统美学与现代医学科技完美融合。应用“尖端技术设备+诊疗手法”为广大求美者提供“时尚+安全”的微整形服务，医院结合美丽与科技，不断创新的医疗美容体系和高品质个性化服务，引领前沿技术。在行业还在批量、流水线式整形时，提倡回归医疗本质，专注医疗技术和效果，为爱美女性提供全方位、个性化的定制医疗美容服务，收到社会各界的广泛赞誉与认可!\r\n','09:00——18:00','o_1a5dr9kht5is1hl72v81h2mal8525515082b8f338.jpg,o_1a5dr9kht5is1hl72v81h2mal8525515085a81bdb.jpg,o_1a5dr9kht5is1hl72v81h2mal8525515093a35155.jpg,o_1a5dr9kht5is1hl72v81h2mal852551508785aaa7.jpg,o_1a5btdcnp1phi1rnc1dpase6vv5ai红蓝光1.JPG,o_1a5btdcnp1phi1rnc1dpase6vv5aiCO2激光.JPG',1),(2,'上海真爱医疗美容医院','02162269000','民营二级医疗美容医院','上海市长宁区延安西路934号','121.431822,31.213147','出身名门，尊贵之享\r\n上海真爱医疗美容医院，前身是境内首家专科医院——上海妇孺医院，源自1935，是专业为女性服务的医院典范。2004年，上海真爱医疗美容医院成立，隶属于上海中医药大学附属曙光医院（三甲），不仅始终传承着1935年的经典，更对自身的服务品质不懈追求，始终站在中国女性需求的最前端。\r\n涅槃重生，突破升级\r\n2014年，上海真爱医疗美容医院华丽转身、专注整形。真爱整形科全线升级，引进世界级医疗设备和器材，多位顶级专家加盟真爱，开创了亚洲品质医美时代、引领高端医美行业的全新突破。\r\n贵宾礼遇，皇室尊享\r\n真爱整形有着曾经对待妇科患者的服务意识基础的存在，“用心服务，用爱塑美”的服务理念本质上区别于其他整形医院。视顾客为亲人，真情相待，是我们给您的全城关爱；一心一意，我们将倾尽所能，为您缔造美丽传奇。','9:00——17:00','o_1a5dogr6mm7c1vd5ue91lkk1j8p282-150302103049516.jpg,o_1a5dogr6mm7c1vd5ue91lkk1j8p282-15030210312aZ.jpg,o_1a5dogr6mm7c1vd5ue91lkk1j8p282-15030210315aZ.jpg,o_1a5dogr6mm7c1vd5ue91lkk1j8p282-1503021031202R.jpg,o_1a5dogr6mm7c1vd5ue91lkk1j8p28zl-04.jpg,o_1a5dogr6mm7c1vd5ue91lkk1j8p28sss-01.jpg',1),(3,'上海天大医疗美容医院','4000139399','业界标杆,VIP五星级管家服务','上海市长宁区中山西路339号','121.411639,31.216086','我院成立于2005年，是上海市唯一一家被评为上海市社会医疗机构皮肤美容优势专科，首家中韩合作的整形外科医院，也是中华见义勇为容貌救护站，第60届世界小姐大赛指定医学美容机构，妙桃隆胸5S特约整形机构，39健康网最受欢迎整形美容医院。下颌整形获得国家专利证书。','9:00——17:30','o_1a5brgtkpeset27s741ufk112j2f24-15052G605401c.JPG,o_1a5brgtkpeset27s741ufk112j2f24-15052G5430D96.JPG,o_1a5brgtkpeset27s741ufk112j2f24-15052G5523L29.JPG,o_1a5brgtkpeset27s741ufk112j2f24-15052G53011921.JPG,o_1a5brgtkpeset27s741ufk112j2f24-15052G51K5547.JPG,o_1a5brgtkpeset27s741ufk112j2f24-15052G5440KC.JPG',1);
/*!40000 ALTER TABLE `hospital` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hospital_user`
--

DROP TABLE IF EXISTS `hospital_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hospital_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `passwd` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `hospital_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `hospital_id` (`hospital_id`),
  CONSTRAINT `hospital_user_ibfk_1` FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hospital_user`
--

LOCK TABLES `hospital_user` WRITE;
/*!40000 ALTER TABLE `hospital_user` DISABLE KEYS */;
INSERT INTO `hospital_user` VALUES (1,'meiweiyang','meiweiyang','2015-11-30 19:39:29',1),(2,'zhenai','zhenai','2015-11-30 19:39:51',2),(3,'tianda','tianda','2015-11-30 19:40:06',3);
/*!40000 ALTER TABLE `hospital_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `orig_price` decimal(10,2) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `sub_cat_id` int(11) NOT NULL,
  `hospital_id` int(11) NOT NULL,
  `photos` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `support_choices` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sold_count` int(11) DEFAULT NULL,
  `item_no` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `doctor_desc` text COLLATE utf8mb4_unicode_ci,
  `surgery_desc` text COLLATE utf8mb4_unicode_ci,
  `has_fee` tinyint(1) DEFAULT NULL,
  `image` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `direct_buy` tinyint(1) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `note` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `use_time` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `hospital_id` (`hospital_id`),
  KEY `sub_cat_id` (`sub_cat_id`),
  KEY `ix_item_item_no` (`item_no`),
  CONSTRAINT `item_ibfk_1` FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`id`),
  CONSTRAINT `item_ibfk_2` FOREIGN KEY (`sub_cat_id`) REFERENCES `item_sub_cat` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item`
--

LOCK TABLES `item` WRITE;
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
INSERT INTO `item` VALUES (1,2200.00,1800.00,5,1,'o_1a5e8s4bf17cgj7v1unaa18tho1操作图.jpg,o_1a5e8s4bf17cgj7v1unaa18tho1案例.jpg','埋线双眼皮打造灵动双眸 魅力无限','1,2,3,5',0,'1',1,'<p><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu0002.png\"/></p><p><br/></p><p>姓名：</p><p>袁磊<br/><br/></p><p>资质：</p><p>主治医师<br/><br/></p><p>简介：<br/>上海美未央美容外科首席注射微整专家，上海九院整形外科硕士，韩国首尔Metro Plastic医院访问学者，上海市科学技术委员会课题撰写人。毕业于上海交通大学医学院附属九院硕士，从事外科整形15年，精细眼鼻整形专家，多次受邀参加韩国、欧美等高峰学术交流会。袁磊主任先后在上海交通大学附属第九人民医院整形外科、上海交通大学附属第三人民医院整形外科、上海市宝山区中心医院整形外科、上海东方医院医疗美容科等公立三甲医院任职多年，2015年被美未央特聘为美未央医院整形外科主诊医生、首席注射微整形专家。临床十余年的实践与学习，让袁主任在眼部、鼻部整形、吸脂、微创注射及内窥镜辅助双平面假体隆胸方面有着得天独厚的优势，特别是引以为豪的注射微整形技术受到广大求美者一致好评。<br/></p>','<p style=\"color: rgb(85, 85, 85);\"><span>个性化设计 打造眼部协调美</span></p><p style=\"color: rgb(85, 85, 85);\">袁磊医生在术前会根据求美者的五官特征，按照人体的三庭五眼的黄金比例，综合眼与眉的距离，长度，厚度等来做综合性的设计，使双眼皮效果达到化，提升面部的整体协调美。<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">创口微小 形态自然<br/>埋线双眼皮的手术方法是在眼皮的部位切开一个容得下缝合线出入的微小切口，然后在皮肤内部进行缝合，将皮肤与提上睑肌腱膜或睑板缝合，形成粘连，从而形成重睑的手术方式。适用于那些眼皮较薄、脂肪较少的求美者。<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">损伤小 恢复快 易修复<br/>由于埋线双眼皮手术切口微小，对组织损伤较小，因此术后浮肿较轻，恢复快。若对双眼皮形状不满意，修复也相对容易。<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">适合人群：</p><p style=\"color: rgb(85, 85, 85);\">内双、眼皮一单一双、眼皮薄、无明显脂肪堆积者<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">治疗方法：</p><p style=\"color: rgb(85, 85, 85);\">手术<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">治疗次数：</p><p style=\"color: rgb(85, 85, 85);\">一次<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">术前准备：<br/>1、术前不要化妆，保持眼部清洁，不要戴隐形眼镜。<br/>2、如有结膜炎、睑缘炎、严重砂眼者必须治愈后才能接受手术。<br/>3、双眼皮手术与近视眼手术之间要相隔至少两个月。<br/>4、双眼皮手术前两周内，请勿服用含有阿斯匹林的药物<br/>5、双眼皮手术前确定身体健康，无传染性疾病或其他身体炎症<br/>6、做双眼皮手术女性要避开月经期。<br/>7、术前准备太阳镜（遮掩伤痕）、冰袋（术后冰敷伤口用）等物品。<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">手术时长：</p><p style=\"color: rgb(85, 85, 85);\">30-40分钟<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">术后是否住院：</p><p style=\"color: rgb(85, 85, 85);\">否<br/><br/>效果展示:<br/><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu114.png\"/></p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">注意事项：<br/>1、术后按医嘱进行冰敷，冰敷可以有效减轻肿胀和疼痛。<br/>2、避免用不干净的手或毛巾等接触手术部位，否则可能导致手术部位细菌感染。<br/>3、按医嘱服用消炎药，发炎后治愈的手术痕迹尤其明显，同时炎症也可能影响双眼皮的形状，所以要注意预防发炎。&#8232;术后尽量垫高头部减轻肿胀<br/>4、术后冷敷只需2-3天左右，之后要热敷。热敷可以帮助血液循环，有助于消肿。<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">常见问题：<br/>Q:埋线双眼皮会留疤痕么?<br/>埋线双眼皮创口微小，愈后痕迹可隐藏在形成双眼皮的褶皱里，肉眼几乎看不出来。<br/>Q:埋线双眼皮能永久保持吗?<br/>埋线可能会有一定的脱落几率，这与医生打结的松紧程度、个人的眼睛条件以及平时的保护等因素有关。一般可维持2年以上。<br/>Q:术后有哪些注意事项?<br/>术后要保持伤口清洁，防止感染，伤口愈合前不要沾水。一个月内忌烟酒，不要吃羊肉、辣椒一类辛辣刺激性食物。<br/></p>',1,'subcaticon/1448862874.94',1,'2015-11-30 14:10:22','费用仅包含手术费、血常规、凝血四项麻醉','需提前一天预约'),(2,5600.00,4800.00,10,1,'o_1a5gli0fv1r7r1pi617dkelh3uv1122121.jpg,o_1a5e75lft2p5l0p1uue1p0j1fete1564d97052faf6.png,o_1a5e8v5f911aco481jor1g4l1vbd13案例图.jpg','伊婉玻尿酸打造饱满柔和年轻面部 做更美的自己','1,2,3,5,6',0,'2',1,'<p style=\"color: rgb(85, 85, 85);\"><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu0002.png\"/></p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">姓名：</p><p style=\"color: rgb(85, 85, 85);\">袁磊<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">资质：</p><p style=\"color: rgb(85, 85, 85);\">主治医师<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">简介：<br/>上海美未央美容外科首席注射微整专家，上海九院整形外科硕士，韩国首尔Metro Plastic医院访问学者，上海市科学技术委员会课题撰写人。毕业于上海交通大学医学院附属九院硕士，从事外科整形15年，精细眼鼻整形专家，多次受邀参加韩国、欧美等高峰学术交流会。袁磊主任先后在上海交通大学附属第九人民医院整形外科、上海交通大学附属第三人民医院整形外科、上海市宝山区中心医院整形外科、上海东方医院医疗美容科等公立三甲医院任职多年，2015年被美未央特聘为美未央医院整形外科主诊医生、首席注射微整形专家。临床十余年的实践与学习，让袁主任在眼部、鼻部整形、吸脂、微创注射及内窥镜辅助双平面假体隆胸方面有着得天独厚的优势，特别是引以为豪的注射微整形技术受到广大求美者一致好评。</p>','<p>伊婉玻尿酸，纯进口，安全!<br/>经过国家CFDA认证的合法玻尿酸，与瑞蓝玻尿酸同为应用较广的进口玻尿酸，伊婉玻尿酸是人体可代谢吸收的合成物，并且有良好的弹性和粘性，注射到体内不易移动，对填充、塑形有较好的固定性，主要用于除皱、塑形、填充、全面部年轻化，符合人体工程学，在注射时更方便。注入人体后一般没有排异反应，对人体无害。所以可以放心使用哦!<br/><br/></p><p>效果立显，不影响工作生活<br/>使用伊婉玻尿酸注射完就可以确定效果，手感也很真实，注射之后稍事休息即可恢复日常的工作和学习，不会影响到正常的社会交往。<br/><br/></p><p>十余年注射经验微整形经验专家亲自操作 技术精湛 给你精致美美五官<br/>玻尿酸注射过程就像上帝在造人一样，专家结合独创扇面“三定”注射技术(定位、定层、定量)，把一支剂针分散来打。随后，医生必须要在打进去的玻尿酸还没有变硬之前，捏出合适的形状，操作简单、快速，能帮你在极短时间内塑形成功。<br/><br/></p><p>适合人群：</p><p>想通过注射改善面部情况等人群<br/><br/></p><p>治疗方法：</p><p>注射<br/><br/></p><p>治疗次数：</p><p>大部分一次成型<br/><br/></p><p>术前准备：</p><p>局部敷麻<br/><br/></p><p>手术时长：</p><p>30-40分钟<br/><br/></p><p>术后是否住院：</p><p>否</p><p><br/></p><p>效果展示：</p><p><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu112.png\"/></p><p><br/><br/>注意事项：<br/>1、强烈建议患者在治疗前至少3—4天内，不要服用消炎药(如阿司匹林等)，因为其有可能会加剧注射部位出血和肿胀。<br/>2、对透明质酸过敏者。<br/><br/></p><p>常见问题：<br/>问：怎么判断我打的玻尿酸是合格产品呢？<br/>答：一般正规机构用的都是合格产品，另外，产品上贴的标签都有防伪标示，可以查询。<br/>问：注射玻尿酸有什么优势?<br/>答：因为玻尿酸是人体自身皮肤组织之一，在人体内停留时间短，会在6-12个月左右被人体分解掉，不会有长期副作用，过敏反应少;注射法，局部仅有微胀微痛感，求美者容易接受。<br/>问：注射玻尿酸术后注意什么?<br/>答：1、在注射后24小时内，为了让外形固定，要避免接触注射区域。<br/>2、如果有服用阿司匹林或其它类似药物，可能会增加瘀青及流血的。因此要避免服用。<br/>3、术后1天可以维持一般基础保养程序，不要额外在治疗部位按摩。这是玻尿酸注意事项中最重要的一项。<br/>4、打玻尿酸后不要在注射部位冰敷或热敷，还要做好防晒。<br/>问：玻尿酸一年进行几次?<br/>答：选用的是可被人体吸收代谢的玻尿酸，随着时间的推移，效果会逐渐消失，一般情况下进行一次玻尿酸能够维持一年左右，而如果想要长久的维持效果，可根据医生提议按期注射。<br/></p>',1,'subcaticon/1448867706.82',1,'2015-11-30 15:24:59','费用仅包含手术费、注射费','需提前一天预约'),(3,7800.00,6800.00,8,1,'o_1a5e90gng1hjf67ehqa1p57guc1k操作图2.jpg,o_1a5e90gng1hjf67ehqa1p57guc1k操作图.jpg,o_1a5e90gng1hjf67ehqa1p57guc1k案例.jpg','硅胶假体隆鼻 搞定立体挺拔美鼻 娇俏鼻型不留痕迹','1,2,3,5',0,'3',1,'<p style=\"color: rgb(85, 85, 85);\"><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu0002.png\"/></p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">姓名：</p><p style=\"color: rgb(85, 85, 85);\">袁磊<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">资质：</p><p style=\"color: rgb(85, 85, 85);\">主治医师<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">简介：<br/>上海美未央美容外科首席注射微整专家，上海九院整形外科硕士，韩国首尔Metro Plastic医院访问学者，上海市科学技术委员会课题撰写人。毕业于上海交通大学医学院附属九院硕士，从事外科整形15年，精细眼鼻整形专家，多次受邀参加韩国、欧美等高峰学术交流会。袁磊主任先后在上海交通大学附属第九人民医院整形外科、上海交通大学附属第三人民医院整形外科、上海市宝山区中心医院整形外科、上海东方医院医疗美容科等公立三甲医院任职多年，2015年被美未央特聘为美未央医院整形外科主诊医生、首席注射微整形专家。临床十余年的实践与学习，让袁主任在眼部、鼻部整形、吸脂、微创注射及内窥镜辅助双平面假体隆胸方面有着得天独厚的优势，特别是引以为豪的注射微整形技术受到广大求美者一致好评。</p>','<p>鼻部综合美学设计</p><p>美未央专家做隆鼻手术不仅是单纯的垫高鼻梁和鼻子单部位的问题，传承东方美女独特的设计，按照美学标准进行多面高精度设，打造出与面部整体和谐的美鼻。</p><p><br/></p><div>精细微创的美鼻手术</div><div>微创的手术方式，让美鼻更轻松，恢复期更短，鼻部形态更自然，最亲密的人都看不出痕迹。<br/><br/></div><div>隆鼻效果自然逼真<br/>术后鼻子宛如天生，无痛无痕，固定持久，玲珑挺翘，从视觉上和触觉上都达到无可挑剔的美学新高度!<br/><br/></div><div>痕迹隐藏 正面完全看不出来<br/>医生会在你的鼻小柱做仅1cm切口，通过精准的剥离骨膜，将假体植入到佳层次，再进行精细缝合，因为切口在鼻下缘，痕迹隐藏，正面完全看不出痕迹来。　　<br/><br/></div><div>适合人群：鼻梁低平，鼻尖低矮，鼻头肥大，想要隆鼻者<br/><br/></div><div>治疗方法：手术<br/><br/></div><div>治疗次数：一次<br/><br/></div><div>术前准备：<br/>1、隆鼻手术前确定身体健康，无传染性疾病或其他身体炎症<br/>2、做隆鼻手术女性要避开月经期。<br/><br/></div><div>手术时长：</div><div>1小时左右<br/><br/></div><div>术后是否住院：</div><div>否<br/><br/></div><div>效果展示<br/><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu数01.png\"/><br/><br/>注意事项：</div><div>1、不要吃刺激性食物;<br/>2、恢复期避免外力挤压鼻子;<br/>3、改掉挖鼻孔、挤黑头等不良生活习惯;<br/>4、定期到医院复查<br/><br/></div><div>常见问题：<br/>Q： 硅胶假体会发生透光吗?<br/>鼻子部位的皮肤是有限的，如果本身鼻部皮肤比较薄，或者放入的假体过大过高，或者层次太浅，鼻头就会容易透光。这就需要医生手术中，合理判断求美者鼻部情况，将假体植入较深层次筋膜下，从而有效降低出现这种情况的可能性。<br/>Q：硅胶假体隆鼻后效果能够维持多长时间，多久需要更换?<br/>因人而异哦，有些可长久维持，但是建议你定期去医院复查，国内也有医生建议，最好十年左右更换硅胶假体。<br/>Q：硅胶假体隆鼻后，歪掉了怎么办?<br/>可以到正规医院进行假体取出的手术，但修复手术要比首次更复杂，所以建议到正规的医院，找经验丰富的医生就诊，他会根据你的自身情况，来设计具体的修复方案哦。<br/><br/></div>',1,'subcaticon/1448870958.6',1,'2015-11-30 16:16:32','费用仅包含手术费、血常规、凝血四项麻醉','需提前一天预约'),(4,4400.00,3800.00,5,1,'o_1a5e97h91kif89a1klg1tpc1fab3v操作图.jpg,o_1a5e97h91kif89a1klg1tpc1fab3v案例.jpg','切开双眼皮手术 打造自然迷人大眼睛','1,2,3,5,6',0,'4',1,'<p><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu11.png\"/></p><p><br/></p><p>姓名：<br/>徐丽娟<br/><br/></p><p>资质：<br/>主诊医生<br/><br/></p><p>简介：<br/>徐丽娟主任从事整形外科临床工作十余年，曾在北京大学深圳医院整形外科工作多年，后在上海工作期间，有幸受过中国整复外科事业的创始人之一、中国工程院院士、上海交通大学医学院终身教授张涤生院士的亲自指导。她是中国医师协会美容与整形医师分会会员，整形外科资深医师，被称为最具亲和力的整形专家，成功参与多项重大、高难度整形术，在整形领域开辟了新的视野。这也使得徐主任在整形行业有着不同于其他医生的见解，徐主任将这些简介研究发表于《中国美容医学》《中华医学杂志》等刊物上，受到业界重视，最终被聘为中国医师协会美容与整形医师分会聘为特别会员。<br/></p>','<p style=\"color: rgb(85, 85, 85);\">★精心设计，制定最佳美眼方案<br/>美未央医疗美容徐丽娟主任会结合求美者眼角的局部结构特点，依据求美者眼部特征以及内眦皮肤纹路定制最佳美眼方案，效果自然，宛若天生。<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">★术前16项眼部评估 手术精确到0.1mm<br/>术前医生会对你的眼部进行全方位评估，如眼睛形态、双眼间距、眉眼间距、眼睛宽高比、五官比例、眼睛宽度、皮肤紧致度、眼窝深浅、内眦情况等16项眼部评估，最终制定最适合你的比例。从而通过切开双眼皮能放大双眼，以其独到的切口轨迹和超精细的手术要求，手术精确到0.1mm，充分依照眼睑的动静态美感。 调整眼间距，使眼睛拉长显亮、睫毛上翘、眼睛形态与面部比例协调，让眼部焕发年轻光彩，闪亮电眼，一步到位。<br/>　　</p><p style=\"color: rgb(85, 85, 85);\"><span>★全方位的美眼术 手法精细切口隐蔽效果更持久</span></p><p style=\"color: rgb(85, 85, 85);\">切开双眼皮沿着皮肤的天然纹理做切口，并做精细操作，手术全程使用的也都是全套的精细器械，同时采用Prolene专业缝针缝线，更加确保术后切口能够更好、更快愈合，痕迹隐藏，效果持久。真正做到精雕双眼皮、一次成形，眼睛更大更有灵气动感。<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">适合人群：</p><p style=\"color: rgb(85, 85, 85);\">用于任何类型、任何年龄的单眼皮，对上眼睑皮肤松弛和上睑臃肿者尤为适宜。<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">治疗方法：</p><p style=\"color: rgb(85, 85, 85);\">手术<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">治疗次数：</p><p style=\"color: rgb(85, 85, 85);\">一次<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">术前准备：<br/>1、术前不要化妆，保持眼部清洁，不要戴隐形眼镜。<br/>2、如有结膜炎、睑缘炎、严重砂眼者必须治愈后才能接受手术。<br/>3、双眼皮手术与近视眼手术之间要相隔至少两个月。<br/>4、双眼皮手术前两周内，请勿服用含有阿斯匹林的药物<br/>5、双眼皮手术前确定身体健康，无传染性疾病或其他身体炎症<br/>6、做双眼皮手术女性要避开月经期。<br/>7、术前准备太阳镜（遮掩伤痕）、冰袋（术后冰敷伤口用）等物品。<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">手术时长：</p><p style=\"color: rgb(85, 85, 85);\">30-40分钟<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">术后是否住院：</p><p style=\"color: rgb(85, 85, 85);\">否<br/></p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">效果展示</p><p style=\"color: rgb(85, 85, 85);\"><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu针4.png\"/></p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">注意事项：<br/>1、术后按医嘱进行冰敷，冰敷可以有效减轻肿胀和疼痛。<br/>2、避免用不干净的手或毛巾等接触手术部位，否则可能导致手术部位细菌感染。<br/>3、按医嘱服用消炎药，发炎后治愈的手术痕迹尤其明显，同时炎症也可能影响双眼皮的形状，所以要注意预防发炎。&#8232;术后尽量垫高头部减轻肿胀<br/>4、术后冷敷只需2-3天左右，之后要热敷。热敷可以帮助血液循环，有助于消肿。<br/><br/>常见问题：<br/>Q：切开双眼皮手术时痛不痛?会不会影响视力?<br/>切开双眼皮手术仅仅在打麻药针的时候有少许痛，打完麻药后，做双眼皮手术时是不会感到明显疼痛。只要到正规整形医院找资深医师做双眼皮手术，一般不会影响视力。<br/>Q：切开双眼皮术后需要注意哪些事<br/>术后要保持伤口清洁，防止感染，在切口愈合前洗脸时注意不要打湿伤口。一个月内忌烟酒，勿食辛辣刺激性食物等。<br/>Q：切开双眼皮手术后会不会发生感染?<br/>切开双眼皮手术方法已经比较成熟了，只要是到正规医院做，消毒措施都是很充分的，发生感染的几率是很低的。术后再遵从医嘱进行护理，一般不会有太大问题。<br/></p>',1,'subcaticon/1448872918.35',1,'2015-11-30 16:53:03','费用仅包含手术费、血常规、凝血四项麻醉','需提前一天预约'),(5,5500.00,4800.00,11,1,'o_1a5e958h8eleb1vj9ngud12u134操作图.jpg,o_1a5e958h8eleb1vj9ngud12u134案例1.jpg','非手术瘦脸 肉毒素塑造上镜玲珑小脸','1,2,3,5,6',0,'5',1,'<p style=\"color: rgb(85, 85, 85);\"><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu0002.png\"/></p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">姓名：</p><p style=\"color: rgb(85, 85, 85);\">袁磊<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">资质：</p><p style=\"color: rgb(85, 85, 85);\">主治医师<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">简介：<br/>上海美未央美容外科首席注射微整专家，上海九院整形外科硕士，韩国首尔Metro Plastic医院访问学者，上海市科学技术委员会课题撰写人。毕业于上海交通大学医学院附属九院硕士，从事外科整形15年，精细眼鼻整形专家，多次受邀参加韩国、欧美等高峰学术交流会。袁磊主任先后在上海交通大学附属第九人民医院整形外科、上海交通大学附属第三人民医院整形外科、上海市宝山区中心医院整形外科、上海东方医院医疗美容科等公立三甲医院任职多年，2015年被美未央特聘为美未央医院整形外科主诊医生、首席注射微整形专家。临床十余年的实践与学习，让袁主任在眼部、鼻部整形、吸脂、微创注射及内窥镜辅助双平面假体隆胸方面有着得天独厚的优势，特别是引以为豪的注射微整形技术受到广大求美者一致好评。</p>','<p style=\"color: rgb(85, 85, 85);\">多点注射见效快</p><p style=\"color: rgb(85, 85, 85);\">衡力注射瘦脸使用微量肉毒素进行面部多点皮下注射，可在短时间内达到理想效果。<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">无需等待，随做随走</p><p style=\"color: rgb(85, 85, 85);\">衡力注射瘦脸是通过肉毒素对咬肌及其支配神经进行麻痹来达到瘦脸的目的，恢复期很短，只消几分钟即可直接回家或去办公室上班，让你的美丽在不</p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">知不觉中自然展现</p><p style=\"color: rgb(85, 85, 85);\">剂量和操作过程、谨慎，比手术价格便宜而更显经济。<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">适合人群：</p><p style=\"color: rgb(85, 85, 85);\"><span>想通过注射改善面部情况等人群</span></p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">治疗方法：</p><p style=\"color: rgb(85, 85, 85);\">注射<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">治疗次数：一次<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">术前准备：局部敷麻<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">手术时长：约10分钟<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">术后是否住院：否<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">效果展示<br/></p><p style=\"color: rgb(85, 85, 85);\"><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu%E4%B8%9401.png\"/></p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">注意事项：<br/>1、做前在一周内不能饮酒<br/>2、两周内服用过阿司匹林或其他解热镇痛药<br/>3、对肉毒毒素制品中任何成分过敏者或过敏体质<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">常见问题：<br/>Q：肉毒素注射有什么副作用吗?<br/>答：有，多为暂时性的。术后常见注射部位肌肉麻痹、肿胀等，常发生在治疗后3-5天，一般2-4周逐渐消退。建议到正规整形医院找专业医生可最大限度的避免。<br/>Q : 肉毒素注射多久可以见效啊?<br/>答：一般1-2周可以见效，个人体质不同也会有所差异。<br/>Q：一次肉毒素注射通常能维持多久呢?<br/>答：通常情况下，一次注射可维持6-12个月左右，为持续维持，可反复注射。建议间隔时间在6个月左右为宜，具体情况请咨询正规医院专业的医生为准，以免引起永久性肌肉麻痹。</p>',1,'subcaticon/1448878789.69',1,'2015-11-30 19:16:30','费用仅包含注射100单位肉毒素','需提前一天预约'),(6,500.00,300.00,12,3,'o_1a5eap8vl1c501uf9ca1nrheaep6-14022615245B54.jpg,o_1a5eap8vl1c501uf9ca1nrheaep5-14030Q2230QH.jpg,o_1a5eap8vl1c501uf9ca1nrheaep5-140314103311F9.jpg','超声波洗牙','1,2,3',0,'6',1,'<h1></h1><h1 style=\"color: gray;\"><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/yisheng/yanjun.jpg\"/></h1><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">姓名：<br/>闫珺<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">资质：<br/>副主任医师，上海天大美容牙科中心主任，国际牙科联盟(FDI)协会会员，国际牙医师院(ICD)专科医师会员，中华口腔医学会会员<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">简介：<br/>从事口腔临床工作20余年，积累了丰富的临床经验，曾先后到四川大学、华西医科大学口腔医学院口腔内科和西安第四军医大学口腔医学院口腔修复科深造。擅长牙周疾病的综合治疗；牙体缺损的微创美学修复；牙列缺损和牙列缺失的美学修复以及牙列不齐的矫治、牙齿美白等美容牙科的治疗。&#65279;</p><p><span></span></p>','<p>超声波洗牙是利用超声波洁牙机机头的高频震动，使牙结石受到震动而松脱。喷砂洁牙是利用高压下喷出的可溶性&#34;细砂&#34;(一种钠盐)，将牙齿表面的烟斑、茶垢、色素快速高效地去除，同时有抛光作用，使牙齿表面光洁亮丽、口内清爽。<br/><br/></p><p>技术优势<br/>安全：对牙齿无损伤，整个过程严格执行无菌操作，通过美国FDA认证。<br/>有效：对牙结石、黄牙、烟斑牙等洗后即可看见卓越的美白效果。<br/>快速：一次洗牙，清洁、保健、美齿只需30分钟。<br/>轻松：不需麻醉，在休闲等待中轻松度过。<br/><br/></p><p>蜕变案例<br/></p><p><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/shanghaitianda/chaoshengboxiya/xiaoguo.jpg\"/></p><p><br/></p><p>注意事项<br/>注意保洁，轻轻刷牙也是成人洗牙后的注意事项。洗牙后要注意牙齿的保洁工作，早晚刷牙，前一周牙齿会比较敏感，因此刷牙时不要太用力。刚洗牙后的牙齿，会因为牙齿间的污垢消失而感到不习惯，或是牙齿轻微松动的错觉。成人洗牙后的注意不要因此频繁地舔弄、吸吮牙齿、牙龈。更不要用手指、牙签拨弄牙齿，以防因此导致出血感染。<br/></p>',1,'subcaticon/1448890069.99',1,'2015-11-30 19:29:13','费用仅包含手术费','需提前1天左右预约'),(7,1200.00,1000.00,4,2,'o_1a5e3etb416g1sbp7tt1mgi1rn49c20150811145324794.jpg,o_1a5e3753kjadiaik09pc1ncn8f20150811145333777.jpg','白瓷娃娃改善肤质 ','1,2,3',0,'7',1,'<p><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu1-14091ZZ132Q3-2.jpg\"/></p><p><br/></p><p>姓名：<br/>孔令义<br/><br/></p><p>资质：<br/>副主任医师<br/><br/></p><p>简介：<br/>从事皮肤临床及激光美容工作二十余年，知名的医学美容专家，韩国Timepeel医院访问学者、客座教授;国内“金手指”美肤技术奖获得者;中国激光面部换肤术(深层嫩肤术)首席专家;国内最早将激光技术应用于皮肤美容领域的专家之一;首创新&#34;靶向美白&#34;治疗黄褐斑及色素疾病;曾获两项国家发明专利、一项自治区科技进步成果奖;中央电视台播音员、主持人私人皮肤美容顾问，曾任东南亚国家及国内多位当红明星金牌皮肤美容顾问。<br/>虽然是业界享誉盛名的&#34;光学美肤圣手&#34;，但是当你和他接触时，却丝毫感觉不到专家的架子，温文尔雅，谦逊温和，身怀绝技但又不露锋芒，能将不堪入目的皮肤起死回生，精湛的技艺、谦虚的态度深受广大求美者喜爱和追捧，大家都愿意把自己的美丽希望托付给他。<br/><br/></p><p>擅长项目：<br/>汽化祛斑、痤疮治疗、彩光嫩肤、射频紧肤除皱、冰点无痛脱毛、皮肤美白；主攻面部深层嫩肤、黄褐斑、抗衰老、面部提升、皮肤光老化以及微整形注射美容。<br/></p>','<p>作用原理：</p><p>通过Q1064超短脉宽模式、ACC1064长脉宽模式、Q1064纯平点阵模式分解皮肤真皮层、真皮深层色素及点状斑，有效祛除皮肤色斑，调节肤色不均，嫩肤美白。&#8232;孔令义医生做白瓷娃娃特点：&#8232;1、无创，非侵入性技术，低疼痛感。&#8232;2、疗效显著，美白、嫩肤、抗衰、收细毛孔、延缓衰老，当次见效，疗程结束后保持时间长，效果明显。<br/><br/></p><p>适合人群：  皮肤粗糙、面色暗沉有斑有细纹<br/><br/></p><p>治疗次数：</p><p>1次，持续改善需3—6次<br/><br/></p><p>术前准备：<br/>近期避免阳光暴晒，不可使用光敏性药物和口服异维A酸。<br/><br/></p><p>手术时长：</p><p>30分钟左右<br/><br/></p><p>术后是否住院：</p><p>否<br/><br/></p><p>效果展示：<br/><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu为3.png\"/><br/><br/>注意事项：<br/>白瓷娃娃治疗后，即刻涂抹红霉素、金霉素或百多邦等消炎药膏，治疗部位不要沾水，术后一周内不要吃辛辣带有刺激性的食物，出门注意防晒。<br/><br/></p>',1,'subcaticon/1448883461.5',1,'2015-11-30 19:46:13','费用仅包含1次白瓷娃娃','需提前一天预约'),(8,2500.00,2000.00,13,3,'o_1a5eanfogjch1g11ru41pic1vkt85-14030Q21405557.jpg,o_1a5eanfogjch1g11ru41pic1vkt85-140314103A4W0.jpg','冷光牙齿美白','1,2,3,5,6',0,'8',1,'<h1><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/yisheng/yanjun.jpg\"/></h1><p><br/></p><p>姓名：<br/>闫珺<br/><br/></p><p>资质：<br/>副主任医师，上海天大美容牙科中心主任，国际牙科联盟(FDI)协会会员，国际牙医师院(ICD)专科医师会员，中华口腔医学会会员<br/><br/></p><p>简介：<br/>从事口腔临床工作20余年，积累了丰富的临床经验，曾先后到四川大学、华西医科大学口腔医学院口腔内科和西安第四军医大学口腔医学院口腔修复科深造。擅长牙周疾病的综合治疗；牙体缺损的微创美学修复；牙列缺损和牙列缺失的美学修复以及牙列不齐的矫治、牙齿美白等美容牙科的治疗。&#65279;<br/></p><p></p>','<p>这种技术是一项正流行于欧美的牙齿美白技术，它不仅可以去除牙齿表面的色素沉积，同时可进入牙齿深层达到脱色的效果。操作过程仅需三十分钟，无副作用，美白效果可维持两年以上。<br/><br/></p><p>技术优势<br/>医院采用的低温冷光，不产生热效应，完全避免了操作过程中对牙神经的刺激，不会引起牙神经的不适，所以牙齿不会有酸胀感觉。医生会在牙齿全面涂抹昂贵、无害的美白材料之后，全口牙齿一次照射，所以大大缩短了美白时间，只需30分钟，就可以迅速美白全口牙齿，美白时间短，感觉轻松，美白效果明显。天大口腔所用的美白材料具有亲水性 ,在美白过程中又完全不接触牙龈，对牙齿结构不会造成任何损害。<br/>医院引进的美白牙齿过程仅需短短几分钟，无刺激、无副作用，冷光牙齿美白效果可维持2年以上。因此被公认是目前最有效及最安全的牙齿脱色技术。<br/><br/></p><p>注意事项<br/>1、冷光美白牙齿后24小时内，牙齿很容易再染上有色物质，必须避免饮用茶、咖啡、可乐、红酒、莓果类饮料、有色牙膏、漱口水等及食用深色食物，同时要避免吸烟。<br/>2、建议患者使用美白牙膏，可减轻冷光美白后食物的再着色。<br/>3、平时饮食也应该尽量减少深色食物，注意口腔卫生，早中晚注意刷牙漱口，保持口腔清洁。<br/></p>',1,'subcaticon/1448888267.3',1,'2015-11-30 19:54:17','费用仅包含手术费','需提前1天左右预约'),(9,4500.00,3800.00,5,2,'o_1a5e6scpf1nvj2oi1qqoua9l0tdl33.png','韩式三点双眼皮 告别眯眯眼 双眼带电做女神','1,2,3,5',0,'9',1,'<p><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu1-140QP95P2423.jpg.png\"/></p><p><br/></p><p>姓名：<br/>腾彦<br/><br/></p><p>资质：<br/>主治医师<br/><br/></p><p>简介：<br/>腾彦医生是上海真爱医院整形专家，2002年毕业于武汉大学医学院临床医学专业，2003年就任于上海九院整形外科。从事医疗美容工作10余年，积累了丰富的临床经验，她是中华医学会整形外科学会会员、国际美容整形外科学会会员、台湾微整形美容医学会会员、国内首批获玻尿酸和BOTOX注射资格证医生，并先后出访美国、韩国、日本和台湾等国。擅长项目：自体脂肪丰胸、微整形、面部年轻化、面部精细整形等。<br/></p>','<p>微创2-3mm切口 放大双眼调整眼形<br/>韩式三点双眼皮是微创双眼皮的一种，是在眼皮上切开三个长度仅有2-3毫米的不连续的微小伤口，由这三个不连续的小伤口抽出眶隔下脂肪并把双眼皮固定，同时可以微调眼睛形状。除了一些皮肤非常松弛的人，一般人群都可以用这种双眼皮手术方法。<br/><br/></p><p>5-7天消肿 1-2个月达到效果<br/>手术时在设计好的双眼皮位置的内、中、外各切开一小口，缝合固定形成双眼皮，腾彦医生经验丰富，操作轻柔，术后5-7天逐渐消肿，1-2个月可见效果<br/><br/>适合人群： </p><p> 单眼皮<br/><br/></p><p>治疗方法：</p><p>手术<br/><br/></p><p>治疗次数：</p><p>一次<br/><br/></p><p>术前准备：<br/>1、术前不要化妆，保持眼部清洁，不要戴隐形眼镜。<br/>2、如有结膜炎、睑缘炎、严重砂眼者必须治愈后才能接受手术。<br/>3、双眼皮手术与近视眼手术之间要相隔至少两个月。<br/>4、双眼皮手术前两周内，请勿服用含有阿斯匹林的药物<br/>5、双眼皮手术前确定身体健康，无传染性疾病或其他身体炎症<br/>6、做双眼皮手术女性要避开月经期。<br/>7、术前准备太阳镜（遮掩伤痕）、冰袋（术后冰敷伤口用）等物品。<br/><br/><br/>手术时长：</p><p>30-40分钟<br/><br/></p><p>术后是否住院：</p><p>否<br/><br/></p><p>效果展示：<br/><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu饿02.png\"/><br/><br/>注意事项：<br/>1、术后按医嘱进行冰敷，冰敷可以有效减轻肿胀和疼痛。<br/>2、避免用不干净的手或毛巾等接触手术部位，否则可能导致手术部位细菌感染。<br/>3、按医嘱服用消炎药，发炎后治愈的手术痕迹尤其明显，同时炎症也可能影响双眼皮的形状，所以要注意预防发炎。&#8232;术后尽量垫高头部减轻肿胀<br/>4、术后冷敷只需2-3天左右，之后要热敷。热敷可以帮助血液循环，有助于消肿。<br/></p>',1,'subcaticon/1448884720.47',1,'2015-11-30 20:05:01','费用仅包含手术费、血常规、凝血四项麻醉','需提前一天预约'),(10,4500.00,3680.00,8,2,'o_1a5e6qbuepni1oat19ll191k1t1kd422.png,o_1a5e6qbuepni1oat19ll191k1t1kd4222.png','假体隆出惊艳鼻型 告别窝瓜脸塌塌鼻','1,2,3,5',0,'10',1,'<p style=\"color: rgb(85, 85, 85);\"><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu1-140QP95P2423.jpg.png\"/></p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">姓名：<br/>腾彦<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">资质：<br/>主治医师<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">简介：<br/>腾彦医生是上海真爱医院整形专家，2002年毕业于武汉大学医学院临床医学专业，2003年就任于上海九院整形外科。从事医疗美容工作10余年，积累了丰富的临床经验，她是中华医学会整形外科学会会员、国际美容整形外科学会会员、台湾微整形美容医学会会员、国内首批获玻尿酸和BOTOX注射资格证医生，并先后出访美国、韩国、日本和台湾等国。擅长项目：自体脂肪丰胸、微整形、面部年轻化、面部精细整形等。</p>','<p>腾彦·国产假体隆鼻治疗特点<br/><br/></p><p>与鼻腔相容性好 较少排异刺激<br/>硅胶假体为高分子硅化物，其有良好的生物相容性。<br/><br/></p><p>可塑性很强 利于雕刻出适合的鼻型<br/>质地较硬，富有弹性，易于加工成型，可塑性极强。<br/><br/></p><p>医生较为熟悉 技术风险较小<br/>来源广泛，成本较低，应用历史更悠久，多数医生对硅胶材料更熟悉，钳夹后不易变形，对医生技术的要求也相对较低，如果再有高水平的医生可谓是事半功倍哦~<br/><br/></p><p>腾医生治疗特点：<br/>1、设计<br/>强调整体和谐，全面设计，精细操作。<br/>2、隐形逼真</p><p>鼻部整体雕塑中心有精品固体硅胶，仿生材料、自体软骨组织等多种隆鼻材料可以选择，手术的超微切口一般选择在鼻小柱或鼻孔内，待把材料植入后，再精细地缝合切口。术后无疤痕，形态自然逼真。<br/>3、自然持久<br/>鼻型与整体面相和谐搭配，效果持久保持。<br/>4、经验丰富<br/>腾彦专家具有20年以上整形经验，确保术后效果超出你的预期。<br/><br/>适合人群： </p><p> 鼻梁低，是鞍鼻、塌鼻<br/><br/></p><p>治疗方法：</p><p>手术<br/><br/></p><p>治疗次数：</p><p>一次<br/><br/></p><p>术前准备：<br/>1、术前两周，要禁烟，禁酒。<br/>2、前两周内，请勿服用含有阿斯匹林的药物<br/>3、患有高血压和糖尿病的患者，应该在初诊时翔实向医生告知病情，以便应诊大夫确认手术方<br/>4、有出血倾向病史的患者要检查血小板和出、凝血时间。<br/><br/>手术时长：</p><p>60分钟<br/><br/></p><p>术后是否住院：</p><p>是<br/></p><p><br/>注意事项：<br/>1、单纯假体植入隆鼻术常规用棉胶粘贴固定鼻背5-7天；<br/>2、术后可视情况而定预防性静脉滴注抗生素2天或口服抗生素3-5天；<br/>3、术后1-2个月内禁止触碰鼻部和戴框架眼镜等，以免假体歪斜。<br/></p>',1,'subcaticon/1448885239.77',1,'2015-11-30 20:12:39','费用仅包含手术费、血常规，感染五项，凝血五项，麻醉','需提前一天预约'),(11,7000.00,5500.00,8,3,'o_1a5c8ta0n84s6j6h6d19apt9b12案例.jpg','隆鼻国产硅胶','1,2,3,5,6',0,'11',1,'<h1></h1><h1 style=\"color: gray;\"><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmuV%201.png\"/></h1><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">姓名：<br/>任天平<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">资质：<br/>副主任医师，上海天大整形外科学科带头人，中国面部精微整形专家，中国非手术面部年轻化技术倡导者，中国专业非手术注射美容专家，国内内窥镜隆胸先行者<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">简介：<br/>从事整形美容临床工作二十余年，在业界享有很高声誉，曾多次与韩日美等整形大师同台手术。经十几年的潜心研究及临床经验，在微整形、面部精雕及隆胸术等整形手术方面都拥有很深的造诣，能将艺术和富有个性的审美观点完美地相结合，为每一位求美的女性朋友进行各种不同要求的整形手术，让她们充满自信和勇气。</p><p><br/></p>','<p>植入体采用与人体组织相容性良好的材料、如硅橡胶、膨体聚四氟乙烯（PTFE）等，这些材料性质稳定、不会与其它物质发生反应；无毒性、致癌性 致畸性；质地柔软并易于雕刻塑形；最大的优点是在手术后、病人认为外型不理想时可以较容易完整地取出，而不会留下缺憾。<br/><br/>技术优势<br/>假体隆鼻手术就是根据我们身体的特点，使用假体材料来帮助我们进行改善，这样就能够让我们的身体得到明显的改善和提升，给人们的形象带来明显的提升和改善效果。通过手术，我们的鼻子就能够得到得到明显的改善，利用这样的方式我们的容貌就能出现明显的改善效果。<br/>上海天大假体隆鼻，在考虑面部五官的整体协调美的基础上，更充分结合个人的气质特征，为您实现面部立体美奠定了坚实的基础。天大以综合鼻整形大师张景涛亲自为每位求美者量鼻定做个性化俏鼻，细腻精巧的微精操作，靓丽鼻型即刻展现!<br/><br/>上海天大假体隆鼻三大优势--缔造美鼻零负担<br/>A、技术优势：天大综合美鼻技术在亚洲医疗美容界首屈一指，遥遥领先;<br/>B、专项优势：上海天大医院术业有专攻，坚持“一对一”的接待模式;<br/>C、效果优势：每一位专家都是在鼻部整形领域独树一帜的专业技术人才。<br/><br/>注意事项</p><p>1、术后不要吃辛辣、刺激的食物。<br/>2、必要时服用抗生素（非必须，遵医嘱）。<br/>3、最好于术后以下时间点来院复查：两天、一周、一个月、三个月以及半年、一年。。<br/>4、保持伤口清洁，一周内避免沾水。<br/>5、注意避免碰撞鼻部，一个月内不能戴框架眼镜。<br/></p>',1,'subcaticon/1448889438.77',1,'2015-11-30 20:14:15','费用仅包含手术费','需提前3天左右预约'),(12,2600.00,1980.00,5,2,'o_1a5e6henqp5a1rh11eicn4p1knucc01.jpg,o_1a5e6henqp5a1rh11eicn4p1knucc02.jpg','埋线双眼皮 不开刀不拆线 双眼保持电力充足','1,2,3',0,'12',1,'<p style=\"color: rgb(85, 85, 85);\"><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu1-140QP95P2423.jpg.png\"/></p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">姓名：<br/>腾彦<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">资质：<br/>主治医师<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">简介：<br/>腾彦医生是上海真爱医院整形专家，2002年毕业于武汉大学医学院临床医学专业，2003年就任于上海九院整形外科。从事医疗美容工作10余年，积累了丰富的临床经验，她是中华医学会整形外科学会会员、国际美容整形外科学会会员、台湾微整形美容医学会会员、国内首批获玻尿酸和BOTOX注射资格证医生，并先后出访美国、韩国、日本和台湾等国。擅长项目：自体脂肪丰胸、微整形、面部年轻化、面部精细整形等。</p>','<p>适合做埋线双眼皮的人群</p><p>该法适用于睑裂大、眼睑薄、无臃肿、眼睑皮肤无松弛而张力正常、无内眦赘皮的年轻人</p><p><br/></p><p><br/></p><div>微调眼部轮廓 放大双眼<br/>埋线双眼皮手术是指通过缝合的方式，直接把缝线（或高分子缝合线）埋藏于皮肤及睑板之间，使上睑皮肤同睑板发生粘连，形成重睑的一种手术。术前可以与医生反复沟通确定方案，依据求美者关于重睑的弧度及宽度等形态要求，即刻便可设计出术后效果形态。<br/><br/></div><div>手术创伤小无需拆线<br/>埋线双眼皮手术只有几个针孔大小的创口，手术过程操作简便、创伤小、消肿快、不需拆线，可以避免二次创伤<br/><br/></div><div>3-5天消肿 1-2个月即可恢复<br/>埋线双眼皮操作简便，只需将一条线埋入设计好的位置，术后一般一周后即可消肿，1-2个月即达到效果。如果恢复过程中效果不满意可在一周后拆除缝线，不用等到几个月之后。<br/><br/>适合人群：</div><div> 单眼皮<br/><br/></div><div>治疗方法：</div><div>埋线<br/><br/></div><div>治疗次数：</div><div>一次<br/><br/></div><div>术前准备：<br/>1、术前两周，要禁烟，禁酒。<br/>2、如有结膜炎、睑缘炎、严重砂眼者必须治愈后才能接受手术。</div><div>3、术前不要化妆，保持眼部清洁，不要戴隐形眼镜。</div><div>4、双眼皮手术与近视眼手术之间要相隔至少两个月。</div><div>5、双眼皮手术前两周内，请勿服用含有阿斯匹林的药物<br/>6、患有高血压和糖尿病的患者，应该在初诊时翔实向医生告知病情，以便应诊大夫确认手术方案双眼皮手术前确定身体健康，无传染性疾病或其他身体炎症<br/>7、做双眼皮手术女性要避开月经期。<br/>8、术前准备太阳镜（遮掩伤痕）、冰袋（术后冰敷伤口用）等物品。<br/>9、有出血倾向病史的患者要检查血小板和出、凝血时间。<br/><br/>手术时长：</div><div>30分钟<br/><br/></div><div>术后是否住院：否<br/><br/>注意事项：<br/>1、刚做完手术，最好用小纱布盖住手术部位，并用冰块进行冷敷，低温会使感觉减弱，减低从麻醉中醒来后可能出现的一点疼痛。需要用塑料袋或塑料泡膜包好冰块轻轻地放在眼睛上面，同时要防止冰块溶化后漏出并进入手术部位而导致细菌感染。</div><div>&#8232;2、避免用不干净的手接触手术部位，否则很有可能导致手术部位细菌感染。&#8232;</div><div>3、按医嘱服用消炎药，发炎后治愈的手术痕迹尤其明显，同时炎症也可能影响双眼皮的形状，所以要注意预防发炎。&#8232;</div><div>4、要注意术后的姿势。例如，低头或趴着看书，会加重肿胀，所以最好仰着头，坐在舒服的椅子上休息;睡觉时也要垫高枕头，这也有助于消肿。</div><div>&#8232;5、术后冷敷只需2-3天左右，之后要热敷。热敷可以帮助血液循环，有助于消肿。<br/><br/><br/></div>',1,'subcaticon/1448885748.13',1,'2015-11-30 20:21:47','费用仅包含血手术费、常规、感染五项、凝血五项、麻醉','需提前一天预约'),(13,9000.00,7900.00,8,3,'o_1a5c8rlfbpd81var8bvp25gqbm鼻部.jpg','隆鼻进口硅胶','1,2,3,5,6',0,'13',1,'<h1 style=\"color: gray;\"><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmuV%201.png\"/></h1><p><br/></p><p>姓名：<br/>任天平<br/><br/></p><p>资质：<br/>副主任医师，上海天大整形外科学科带头人，中国面部精微整形专家，中国非手术面部年轻化技术倡导者，中国专业非手术注射美容专家，国内内窥镜隆胸先行者<br/><br/></p><p>简介：<br/>从事整形美容临床工作二十余年，在业界享有很高声誉，曾多次与韩日美等整形大师同台手术。经十几年的潜心研究及临床经验，在微整形、面部精雕及隆胸术等整形手术方面都拥有很深的造诣，能将艺术和富有个性的审美观点完美地相结合，为每一位求美的女性朋友进行各种不同要求的整形手术，让她们充满自信和勇气。<br/></p>','<p style=\"color: rgb(85, 85, 85);\"></p><p>植入体采用与人体组织相容性良好的材料、如硅橡胶、膨体聚四氟乙烯（PTFE）等，这些材料性质稳定、不会与其它物质发生反应；无毒性、致癌性 致畸性；质地柔软并易于雕刻塑形；最大的优点是在手术后、病人认为外型不理想时可以较容易完整地取出，而不会留下缺憾。</p><p><br/></p><p>技术优势</p><p>假体隆鼻手术就是根据我们身体的特点，使用假体材料来帮助我们进行改善，这样就能够让我们的身体得到明显的改善和提升，给人们的形象带来明显的提升和改善效果。通过手术，我们的鼻子就能够得到得到明显的改善，利用这样的方式我们的容貌就能出现明显的改善效果。</p><p><br/></p><p>上海天大假体隆鼻，在考虑面部五官的整体协调美的基础上，更充分结合个人的气质特征，为您实现面部立体美奠定了坚实的基础。天大以综合鼻整形大师张景涛亲自为每位求美者量鼻定做个性化俏鼻，细腻精巧的微精操作，靓丽鼻型即刻展现!</p><p><br/></p><p>上海天大假体隆鼻三大优势--缔造美鼻零负担</p><p>A、技术优势：天大综合美鼻技术在亚洲医疗美容界首屈一指，遥遥领先;</p><p>B、专项优势：上海天大医院术业有专攻，坚持“一对一”的接待模式;</p><p>C、效果优势：每一位专家都是在鼻部整形领域独树一帜的专业技术人才。</p><p><br/></p><p>注意事项：</p><p>1、术后不要吃辛辣、刺激的食物。</p><p>2、必要时服用抗生素（非必须，遵医嘱）。</p><p>3、最好于术后以下时间点来院复查：两天、一周、一个月、三个月以及半年、一年。。</p><p>4、保持伤口清洁，一周内避免沾水。</p><p>5、注意避免碰撞鼻部，一个月内不能戴框架眼镜。</p><p style=\"color: rgb(85, 85, 85);\"></p>',1,'subcaticon/1448888037.91',1,'2015-11-30 20:23:57','费用仅包含手术费','需提前3天左右预约'),(14,3500.00,2800.00,10,3,'o_1a5c5t4je13oq27s1qt61rhpue01q8-14030Q04522Y8.jpg,o_1a5c5t4je13oq27s1qt61rhpue01q8-14030Q04550J8.jpg,o_1a5c5t4je13oq27s1qt61rhpue01q8-14030Q04614V8.jpg','润百颜玻尿酸 丰面颊 丰下巴 丰苹果肌','1,2,3,5,6',0,'14',1,'<h1><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/shanghaitianda/yisheng/minghui.jpg\"/></h1><p><br/></p><p>姓名：<br/>明慧<br/><br/></p><p>资质：<br/>上海天大美容皮肤科学科带头人<br/>明星专属私人形象管理顾问<br/>中国微整形美容专家<br/>中华医学会医学美学分会会员<br/>中国医师协会美容医师分会会员<br/>上海激光医学学会会员<br/><br/></p><p>简介：<br/>在激光美容术、激光嫩肤除皱、激光祛色素斑等激光美容，对微创、无创抗衰老、非手术注射美容等有较深造诣。<br/></p>','<p>丰面颊又称面颊部填充术，面部消瘦给人感觉高度营养不良或长期患有慢性消耗性疾病，由于消瘦显得颧骨高，与同龄人比较，面型呈老化感。丰面颊通过颞部、面部填充使脸型得到改善，而且年轻化。<br/><br/></p><p>注射丰下巴是通过注射的方式将丰下巴的材料注入爱美者的下巴处，达到改变脸型的效果，通过针剂注入脸部，可以见效，无复原期，注射后不影响日常工作和生活。见效快，效果好，安全性高，创伤小，是您丰下巴的最佳选择。<br/><br/></p><p>很多漂亮女人，就算五官长得很细致、皮肤也不错，但只要脸上少了“苹果肌”，就会呈现过度削瘦的面相，即使化妆时再努力上腮红，也画不出苹果肌的甜美效果，让人有难以亲近的感觉。尤其是颧骨位置若较少脂肪，整体给人感觉有棱有角、不易亲近。因此采用注射大分子玻尿酸的方式来丰苹果肌的方式成为很多爱美女士的选择。<br/><br/>技术优势<br/>丰满的皮肤有讨喜或亲和力佳的好处，如何丰面颊、下巴、苹果肌而更有效安全呢，相对于假体，注射而不不开刀会是很多人的理想选择。注射到人体内的生物材料制剂，非常安全，不会对人体产生任何副作用。<br/>注射丰面颊、下巴、苹果肌采用的注射材料为玻尿酸、胶原蛋白、爱贝芙等注射填充材料，非生物源性，与人体相容性极好，不会产生副作用，注射后由专业医生为求美者呈现饱满皮肤。<br/><br/>1、三重认证 倍感安心<br/>上海天大医疗美容医院，我们只使用通过了美国FDA、欧盟CE、中国SFDA三大世界先进资深机构认证的安全产品，确保最高品质的注射效果。<br/>2、个性定制 专属设计<br/>首创“整体化形象设计”概念，即根据爱美者年龄、身高、体重、形象气质与职业特点，为您度身定制专属注射丰面颊、下巴、苹果肌方案，风格精细轻柔，成型效果持久稳固、手感逼真;真正悄悄变美，隐形自然。<br/>3、无创美颜 终极利器<br/>精细到0.1mm微创入路，快速、无痕、无痛，无不适感和肿胀，不需要恢复期，随做随走，不影响工作和生活，尽享精致蜕变的奇迹感受!<br/>4、国际专家 引领标准<br/>拥有国际一流专家团队，平均20年整形临床经验，定期与世界资深专技型整形顾问开展学术交流座谈，同台竞技;风格以“微创、精细”为特色， 强调长期、持久的自然美。<br/><br/>注意事项<br/>1、注射后6小时内，请尽量避免接触注射区域。可轻柔使用水及肥皂清洁，同时轻微的卸妆是可被允许的。<br/>2、注射后，不要曝晒治疗区域于极热状态，如日光浴或日晒或处于极冷处。<br/>3、注射后，可请患者做湿敷(或冰面膜)以减轻不适感。<br/></p>',1,'subcaticon/1448889491.8',1,'2015-11-30 20:46:00','费用仅包含手术费','需提前1天左右预约'),(15,5000.00,4000.00,10,3,'o_1a5c71do61mev3ba1ursgb6go42s8-14022F95HC15.jpg,o_1a5c71do61mev3ba1ursgb6go42s8-140314143401921.jpg,o_1a5c71do61mev3ba1ursgb6go42s8-140314143424540.jpg','瑞兰玻尿酸 丰面颊 丰下巴 丰苹果肌','1,2,3,5,6',0,'15',1,'<h1 style=\"color: gray;\"><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/shanghaitianda/yisheng/minghui.jpg\"/></h1><p><br/></p><p>姓名:<br/>明慧<br/><br/></p><p>资质:<br/>上海天大美容皮肤科学科带头人<br/>明星专属私人形象管理顾问<br/>中国微整形美容专家<br/>中华医学会医学美学分会会员<br/>中国医师协会美容医师分会会员<br/>上海激光医学学会会员<br/><br/></p><p>简介<br/>在激光美容术、激光嫩肤除皱、激光祛色素斑等激光美容，对微创、无创抗衰老、非手术注射美容等有较深造诣。<br/></p>','<p>丰面颊又称面颊部填充术，面部消瘦给人感觉高度营养不良或长期患有慢性消耗性疾病，由于消瘦显得颧骨高，与同龄人比较，面型呈老化感。丰面颊通过颞部、面部填充使脸型得到改善，而且年轻化。<br/>注射丰下巴是通过注射的方式将丰下巴的材料注入爱美者的下巴处，达到改变脸型的效果，通过针剂注入脸部，可以见效，无复原期，注射后不影响日常工作和生活。见效快，效果好，安全性高，创伤小，是您丰下巴的最佳选择。<br/>很多漂亮女人，就算五官长得很细致、皮肤也不错，但只要脸上少了“苹果肌”，就会呈现过度削瘦的面相，即使化妆时再努力上腮红，也画不出苹果肌的甜美效果，让人有难以亲近的感觉。尤其是颧骨位置若较少脂肪，整体给人感觉有棱有角、不易亲近。因此采用注射大分子玻尿酸的方式来丰苹果肌的方式成为很多爱美女士的选择。<br/><br/>技术优势<br/>丰满的皮肤有讨喜或亲和力佳的好处，如何丰面颊、下巴、苹果肌而更有效安全呢，相对于假体，注射而不不开刀会是很多人的理想选择。注射到人体内的生物材料制剂，非常安全，不会对人体产生任何副作用。<br/>注射丰面颊、下巴、苹果肌采用的注射材料为玻尿酸、胶原蛋白、爱贝芙等注射填充材料，非生物源性，与人体相容性极好，不会产生副作用，注射后由专业医生为求美者呈现饱满皮肤。<br/><br/>1、三重认证 倍感安心<br/>上海天大医疗美容医院，我们只使用通过了美国FDA、欧盟CE、中国SFDA三大世界先进资深机构认证的安全产品，确保最高品质的注射效果。<br/>2、个性定制 专属设计<br/>首创“整体化形象设计”概念，即根据爱美者年龄、身高、体重、形象气质与职业特点，为您度身定制专属注射丰面颊、下巴、苹果肌方案，风格精细轻柔，成型效果持久稳固、手感逼真;真正悄悄变美，隐形自然。<br/>3、无创美颜 终极利器<br/>精细到0.1mm微创入路，快速、无痕、无痛，无不适感和肿胀，不需要恢复期，随做随走，不影响工作和生活，尽享精致蜕变的奇迹感受!<br/>4、国际专家 引领标准<br/>拥有国际一流专家团队，平均20年整形临床经验，定期与世界资深专技型整形顾问开展学术交流座谈，同台竞技;风格以“微创、精细”为特色， 强调长期、持久的自然美。<br/><br/>注意事项<br/>1、注射后6小时内，请尽量避免接触注射区域。可轻柔使用水及肥皂清洁，同时轻微的卸妆是可被允许的。<br/>2、注射后，不要曝晒治疗区域于极热状态，如日光浴或日晒或处于极冷处。<br/>3、注射后，可请患者做湿敷(或冰面膜)以减轻不适感。<br/></p>',1,'subcaticon/1448888128.31',1,'2015-11-30 20:53:55','费用仅包含手术费','需提前1天左右预约'),(16,1400.00,1000.00,9,2,'o_1a5e6frolt3hpalbntuknufbr01.jpg,o_1a5e6frolt3hpalbntuknufbr02.jpg','月光真空脱腋毛 ','1,2,3',0,'16',1,'<p style=\"color: rgb(85, 85, 85);\"><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu1-14091ZZ132Q3-2.jpg\"/></p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">姓名：<br/>孔令义<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">资质：<br/>副主任医师<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">简介：<br/>从事皮肤临床及激光美容工作二十余年，知名的医学美容专家，韩国Timepeel医院访问学者、客座教授;国内“金手指”美肤技术奖获得者;中国激光面部换肤术(深层嫩肤术)首席专家;国内最早将激光技术应用于皮肤美容领域的专家之一;首创新&#34;靶向美白&#34;治疗黄褐斑及色素疾病;曾获两项国家发明专利、一项自治区科技进步成果奖;中央电视台播音员、主持人私人皮肤美容顾问，曾任东南亚国家及国内多位当红明星金牌皮肤美容顾问。<br/>虽然是业界享誉盛名的&#34;光学美肤圣手&#34;，但是当你和他接触时，却丝毫感觉不到专家的架子，温文尔雅，谦逊温和，身怀绝技但又不露锋芒，能将不堪入目的皮肤起死回生，精湛的技艺、谦虚的态度深受广大求美者喜爱和追捧，大家都愿意把自己的美丽希望托付给他。<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">擅长项目：<br/>汽化祛斑、痤疮治疗、彩光嫩肤、射频紧肤除皱、冰点无痛脱毛、皮肤美白；主攻面部深层嫩肤、黄褐斑、抗衰老、面部提升、皮肤光老化以及微整形注射美容。</p>','<p style=\"color: rgb(85, 85, 85);\">月光真空脱毛仪通过美国FDA和中国CFDA的严格审批，它大的特点是采用了真空技术，用负压将皮肤轻轻吸进治疗头，这一技术带来了以下3方面的改进：&#8232;1、皮肤痛感更小&#8232;皮肤被吸引，从而拉伸变薄，降低了皮肤黑色素的密度，相对减少了激光能量对表皮黑色素的刺激，皮肤疼痛感更小。&#8232;2、脱毛效果更好&#8232;真空压力暂时压迫皮肤组织和周围血管，减少氧合血红蛋白和色基对激光能量的竞争性吸收，使更多能量被毛囊里面的黑色素吸收，脱毛效果更彻底。&#8232;3、脱毛效率更高&#8232;真空脱毛仪的治疗光斑扩大至22*35MM，光斑覆盖的皮肤面积较大，大大提高了脱毛效率。缩短了治疗时间。例如脱腋毛，15-30min即可完成。<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">适合人群： </p><p style=\"color: rgb(85, 85, 85);\"> 有腋毛困扰的人群<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">治疗方法：</p><p style=\"color: rgb(85, 85, 85);\">激光<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">治疗次数：</p><p style=\"color: rgb(85, 85, 85);\">3-6次<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">手术时长：</p><p style=\"color: rgb(85, 85, 85);\">30分钟<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">术后是否住院：</p><p style=\"color: rgb(85, 85, 85);\">否</p>',1,'subcaticon/1448888749.61',1,'2015-11-30 21:13:24','费用仅包含手术费','需提前1天左右预约'),(17,9500.00,7776.00,10,2,'o_1a5e6avtj1ujj6onb51l49a7tak01.jpg,o_1a5e6avtj1ujj6onb51l49a7tak02.jpg,o_1a5e6avtj1ujj6onb51l49a7tak03.jpg','瑞蓝玻尿酸垫下巴 打造尖翘下巴 让脸型更加美丽','1,2,3,5,6',0,'17',1,'<p><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu请7.png\"/></p><p><br/></p><p>姓名：</p><p>王屏</p><p><br/></p><div>资质：<br/>主任医师<br/><br/></div><div>简介：<br/>毕业于四川泸州医学院，曾在“三甲”医院从事整形临床外科工作20余年，专修于国际著名的北京大学附属第三医院和北京黄寺美容专科医院，2003年成为我国首届医学美容美学设计研究生。<br/>王主任有着丰富的整形美容临床经验和操作技能，对于“美容平面”“黄金分割”等人体美学理论有很深的造诣，完美的将美学设计的理论融入到日常的整形美容实践中，术前的个性化设计，力求将视觉艺术与现代医术结合达到更深层次的审美境界。多次应邀参加韩国美国等国际学术交流，在业界权威期刊上发表学术论文十余篇。</div>','<p>王屏医生治疗特点<br/>20余年临床经验，个性化设计，拉长下巴，让脸型更加漂亮<br/>王屏医生从事整形临床外科工作20余年，有着丰富的医美经验，术前会针对你的情况，进行个性化设计，丰满下巴，让脸型更加漂亮。<br/><br/></p><p>瑞蓝玻尿酸特点<br/>经多国机构认证，使用更加放心，质量点赞！<br/>瑞蓝玻尿酸是由瑞士Q-Med公司生产，已经取得美国FDA认证和中国CFDA认证，质量值得信赖。<br/>原料与人体成分相似，适应性强，不必担心过敏哟~<br/>瑞蓝玻尿酸是一种水晶般透明的凝胶，它的主要成分是透明质酸，同人体内部的天然透明质酸几乎完全一致，使用前无需经过皮肤测试。<br/>不仅可以垫下巴，还能美容补水哦~<br/>在人体内广泛分布着玻尿酸它具有强大的锁水功能，是一种天然保湿因子。而医用注射的玻尿酸是人体玻尿酸相似物，它在代谢的过程中，会结合水取代逐渐减少的容积，使下巴的皮肤变得水水嫩嫩的。<br/><br/>适合人群：</p><p>下巴短小、后缩  <br/><br/></p><p>治疗方法：</p><p>注射<br/><br/></p><p>治疗次数：</p><p>两次<br/><br/></p><p>手术时长：</p><p>10分钟左右<br/><br/></p><p>术后是否住院：</p><p>否<br/><br/></p><p>效果展示：<br/><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu请5.png\"/></p><p><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu请6.png\"/><br/><br/></p><p>注意事项：<br/>注射部位可能红肿，一般3天左右恢复，少数出现青紫现象，1周可恢复。注射后即刻能上班，1天后洗脸，3-5天能化妆<br/></p>',1,'subcaticon/1448936297.29',1,'2015-12-01 10:50:20','费用仅包含手术费','需提前1天预约'),(18,980.00,680.00,3,2,'o_1a5e6d6ni14491gkv12431buk1s8jba01jpg,o_1a5e6d6ni14491gkv12431buk1s8jba02.jpg','综合祛痘 彻底告别痘痘 还原平滑美肌','1,2,3',0,'18',1,'<p style=\"color: rgb(85, 85, 85);\"><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu1-14091ZZ132Q3-2.jpg\"/></p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">姓名：<br/>孔令义<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">资质：<br/>副主任医师<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">简介：<br/>从事皮肤临床及激光美容工作二十余年，知名的医学美容专家，韩国Timepeel医院访问学者、客座教授;国内“金手指”美肤技术奖获得者;中国激光面部换肤术(深层嫩肤术)首席专家;国内最早将激光技术应用于皮肤美容领域的专家之一;首创新&#34;靶向美白&#34;治疗黄褐斑及色素疾病;曾获两项国家发明专利、一项自治区科技进步成果奖;中央电视台播音员、主持人私人皮肤美容顾问，曾任东南亚国家及国内多位当红明星金牌皮肤美容顾问。<br/>虽然是业界享誉盛名的&#34;光学美肤圣手&#34;，但是当你和他接触时，却丝毫感觉不到专家的架子，温文尔雅，谦逊温和，身怀绝技但又不露锋芒，能将不堪入目的皮肤起死回生，精湛的技艺、谦虚的态度深受广大求美者喜爱和追捧，大家都愿意把自己的美丽希望托付给他。<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">擅长项目：<br/>汽化祛斑、痤疮治疗、彩光嫩肤、射频紧肤除皱、冰点无痛脱毛、皮肤美白；主攻面部深层嫩肤、黄褐斑、抗衰老、面部提升、皮肤光老化以及微整形注射美容。</p>','<p style=\"color: rgb(85, 85, 85);\">● 专业医生 量身定制治疗方案 </p><p style=\"color: rgb(85, 85, 85);\">为你解决痘痘困扰&#8232;孔令义医生拥有丰富的光电治疗经验，治疗前，他会根据每个求美者的体质特征、痘痘状况及求美需求，量身定制治疗方案，为你解决痘痘困扰。&#8232;</p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">● 综合治疗 内调外治 抗菌消炎 根源遏制 </p><p style=\"color: rgb(85, 85, 85);\">全效祛痘&#8232;孔令义医生在治疗痘痘时，先采用综合离子雾化理疗、冷喷、超声波药物导入等对产生青春痘的部位进行杀菌消炎，加速局部微循环，杀死导致青春痘的多种细菌；然后采用点阵光学、纳米波等技术进行全面治疗，达到杀菌、排毒、除疤的治疗效果，后通过真爱调配的药膏调理，修复皮肤胶原蛋白，改善皮肤瑕疵，达到全面祛痘、除印、美白的功效。</p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">&#8232;● 更新肤质 分层调配 </p><p style=\"color: rgb(85, 85, 85);\">不仅祛痘更能美肤&#8232;上海真爱美容医院在治疗痘痘时，根据每个求美者的痘痘情况，采用不同的治疗方案，祛痘同时刺激胶角质层更新，祛痘、嫩肤、美白、平坑四效合一，更新肤质，不仅祛痘更能美肤。<br/><br/>适合人群：</p><p style=\"color: rgb(85, 85, 85);\">轻度、中度痘痘<br/><span><br/></span></p><p style=\"color: rgb(85, 85, 85);\"><span>治疗次数：</span></p><p style=\"color: rgb(85, 85, 85);\"><span>一次</span></p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">术前准备：<br/>在治疗当天，需要仔细清洁面部，不能有化妆品残留，以防引发感染，保持一个轻松的心情。<br/><br/>手术时长：</p><p style=\"color: rgb(85, 85, 85);\">30分钟<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">术后是否住院：</p><p style=\"color: rgb(85, 85, 85);\">否</p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">注意事项：<br/>治疗后的12-24小时内，尽量不沾水，不使用洗面奶，以免伤害新生肌肤。治疗后一个月内注意保湿和防晒，建议选择敷面膜的形式进行补水保湿，外出时注意防晒。</p>',1,'subcaticon/1448941876.19',1,'2015-12-01 11:56:42','费用仅包含手术费','需提前一天预约'),(19,6800.00,5000.00,4,1,'o_1a5glkled1gp5dof1u111ue0mpgd233.jpg,o_1a5ef2ir0a6h1kegm871ap91mgr8操作图.jpg,o_1a5ef2ir0a6h1kegm871ap91mgr8仪器.JPG,o_1a5ef2ir0a6h1kegm871ap91mgr8案例.jpg','进口水光注射深层补水 一次注射等于1千次面膜','1,2,3,5,6',0,'19',1,'<p><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu水光珍.png\"/></p><p><br/>姓名：<br/>石文瑞<br/><br/></p><p>资质：<br/>主治医生<br/><br/></p><p>简介：<br/>石文瑞熟练操作每一台激光仪器，对技术有着娴熟的把握操控，尤其是除皱方面有着很深的造诣，她认为，皮肤的每一层次都有着不同的结构质地，而采用的仪器和使用的方法都不相同，在做美肤整形之前，要对皮肤有着很深的了解，深度的剖析才可以更好的把握美肤仪器的操控。水光针注射、U美极抗衰治疗，激光脱毛、激光除色素痣、王者风范嫩肤、像束激光疤痕修复、痤疮治疗、激光祛斑、祛纹身、敏感性皮肤治疗及全身各部位射频除皱紧肤治疗，微整形抗衰老治疗及注射填充塑形等。<br/></p>','<p>通过国际与CFDA认证，可放心使用<br/>水光注射的材料——玻尿酸，是国际公认的较安全的注射材料，玻尿酸又名透明质酸，本身是一种构成人体的天然物质，所以对人体极少有副作用和排斥反应。注射后稳定、自然，又可被吸收，早已获得获食品药品检验局批准进入中国。它是世界非手术美容技术研究中心的推荐产品。<br/>　　</p><p>水光注射的操作方法，非手术方式，无需恢复期</p><p>水光注射采用的是非手术方式，通过注射的方式为肌肤补充水分，无需开刀就能改善皱纹，保湿肌肤，改善暗沉粗糙的皮肤。整个治疗过程较为简单快速，注射后无浮肿，即可恢复日常生活，是时下非常流行的美容护肤疗法。<br/>　　</p><p>水光注射的适应范围广，让你与明星同在<br/>水光注射能够有效改善肤质，让肌肤重回年轻态，适合各种肤质类型，就连敏感类型的肤质也可以做水光注射。在韩国娱乐圈内，已经被艺人们当做&#34;日常护肤之宝&#34;，在台湾、香港的演艺圈内也成为众所周知的秘密。<br/><br/></p><p>适合人群：</p><p>皮肤干燥，面部有细小皱纹，皮肤暗沉、无光泽<br/><br/></p><p>治疗方法：</p><p>注射<br/><br/></p><p>治疗次数：</p><p>1次<br/><br/></p><p>术前准备：</p><p>避开月经期。<br/><br/></p><p>手术时长：</p><p>20分钟左右<br/><br/></p><p>术后是否住院：</p><p>否<br/><br/></p><p>效果展示：</p><p><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu案例.jpg\"/></p><p><br/>注意事项：<br/>1、注射后一周内禁酒禁烟。<br/>2、注射后一周内尽量避开强烈的紫外线。<br/>3、 注射后5天内尽量避免桑拿或剧烈的运动 。<br/>4、 注射后注意不要用力磨擦治疗部位。<br/><br/></p><p>常见问题：<br/>Q：水光针注射时疼吗?<br/>可能会有些痛，不过痛感是可以忍受的，而且如果注射面积较大，医生会为你采取表面麻醉，痛感可明显减轻，如果你特别怕痛，可以要求医生为你做表面麻醉，不过术后麻药劲儿过后会有些红肿，一般注射后3天左右疼痛可逐渐缓解。<br/>Q：水光针注射需多次治疗吗?隔多久做一次?<br/>水光针治疗每次有每次的效果，想要持续保持水嫩效果，一般间隔1-2个月做一次，做完一个疗程三次以后效果可以维持1年左右的时间。<br/>Q：注射后能洗脸吗?<br/>在注射后24-48小时内，最好不要让注射部位与水接触，以免引发感染哦。<br/></p>',1,'subcaticon/1448963426.9',1,'2015-12-01 18:00:07','费用仅包1次水光针注射','需提前一天预约'),(20,8000.00,6800.00,10,1,'o_1a5el5vs9e8gff31vta1bjvgam1f操作图.jpg,o_1a5el5vs9e8gff31vta1bjvgam1f案例.jpg','瑞蓝玻尿酸注射美容 打造精致立体饱满面容','1,2,3,5,6',0,'1512016513',1,'<p style=\"color: rgb(85, 85, 85);\"><img src=\"http://7xnpdb.com2.z0.glb.qiniucdn.com/xiangmu0002.png\"/></p><p style=\"color: rgb(85, 85, 85);\"><br/></p><p style=\"color: rgb(85, 85, 85);\">姓名：</p><p style=\"color: rgb(85, 85, 85);\">袁磊<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">资质：</p><p style=\"color: rgb(85, 85, 85);\">主治医师<br/><br/></p><p style=\"color: rgb(85, 85, 85);\">简介：<br/>上海美未央美容外科首席注射微整专家，上海九院整形外科硕士，韩国首尔Metro Plastic医院访问学者，上海市科学技术委员会课题撰写人。毕业于上海交通大学医学院附属九院硕士，从事外科整形15年，精细眼鼻整形专家，多次受邀参加韩国、欧美等高峰学术交流会。袁磊主任先后在上海交通大学附属第九人民医院整形外科、上海交通大学附属第三人民医院整形外科、上海市宝山区中心医院整形外科、上海东方医院医疗美容科等公立三甲医院任职多年，2015年被美未央特聘为美未央医院整形外科主诊医生、首席注射微整形专家。临床十余年的实践与学习，让袁主任在眼部、鼻部整形、吸脂、微创注射及内窥镜辅助双平面假体隆胸方面有着得天独厚的优势，特别是引以为豪的注射微整形技术受到广大求美者一致好评。</p>','<p>通过FDA、CFDA认证，质量有保证 千万人正在使用<br/>瑞蓝玻尿酸是荣获FDA及CFDA双重认证的注射用玻尿酸产品。目前瑞蓝在全球范围内已有超过千万人次使用，打造自然面孔，质量有保障。<br/>　　</p><p>瑞蓝玻尿酸的效果比较自然<br/>它采用独有的NASHA®专利技术，使其透明质酸成分接近于人体天然透明质酸，结构稳定，注射后组织相容性好因此塑形效果较好。由于瑞蓝玻尿酸的功效并非永久性的，避免了因为面部随时间推移从而产生的外貌永久性改变的遗憾。<br/>　　</p><p>非动物性来源的瑞蓝玻尿酸<br/>瑞蓝为非动物性来源透明质酸，因此引发过敏反应或动物病菌的几率都很低。自体可吸收代谢玻尿酸。<br/>　　</p><p>精准把握注射层次和剂量 快速实现饱满立体</p><p>医生在操作玻尿酸丰唇时，非常熟悉皮肤解剖结构，精准把握注射剂量和层次，快速实现饱满立体效果。<br/><br/></p><p>适合人群：</p><p>想通过注射改善面部情况等人群<br/><br/></p><p>治疗方法：</p><p>注射<br/><br/></p><p>治疗次数：</p><p>大部分一次成型<br/><br/></p><p>术前准备：</p><p>局部敷麻<br/><br/></p><p>手术时长：</p><p>30-40分钟<br/><br/></p><p>术后是否住院：</p><p>否<br/></p><p><br/>注意事项：<br/>1、强烈建议患者在治疗前至少3—4天内，不要服用消炎药(如阿司匹林等)，因为其有可能会加剧注射部位出血和肿胀。<br/>2、对透明质酸过敏者。<br/><br/></p><p>常见问题：<br/>问：怎么判断我打的玻尿酸是合格产品呢？<br/>答：一般正规机构用的都是合格产品，另外，产品上贴的标签都有防伪标示，可以查询。<br/>问：注射玻尿酸有什么优势?<br/>答：因为玻尿酸是人体自身皮肤组织之一，在人体内停留时间短，会在6-12个月左右被人体分解掉，不会有长期副作用，过敏反应少;注射法，局部仅有微胀微痛感，求美者容易接受。<br/>问：注射玻尿酸术后注意什么?<br/>答：1、在注射后24小时内，为了让外形固定，要避免接触注射区域。<br/>2、如果有服用阿司匹林或其它类似药物，可能会增加瘀青及流血的。因此要避免服用。<br/>3、术后1天可以维持一般基础保养程序，不要额外在治疗部位按摩。这是玻尿酸注意事项中最重要的一项。<br/>4、打玻尿酸后不要在注射部位冰敷或热敷，还要做好防晒。<br/>问：玻尿酸一年进行几次?<br/>答：选用的是可被人体吸收代谢的玻尿酸，随着时间的推移，效果会逐渐消失，一般情况下进行一次玻尿酸能够维持一年左右，而如果想要长久的维持效果，可根据医生提议按期注射。<br/></p>',1,'subcaticon/1448969744.72',1,'2015-12-01 19:39:25','费用仅包含手术费、注射费','需提前一天预约');
/*!40000 ALTER TABLE `item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_cat`
--

DROP TABLE IF EXISTS `item_cat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item_cat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_cat`
--

LOCK TABLES `item_cat` WRITE;
/*!40000 ALTER TABLE `item_cat` DISABLE KEYS */;
INSERT INTO `item_cat` VALUES (1,'皮肤',0),(2,'眼部',0),(3,'鼻部',0),(4,'毛发',0),(5,'微整形',0),(6,'口腔',0);
/*!40000 ALTER TABLE `item_cat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_comment`
--

DROP TABLE IF EXISTS `item_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `photos` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `content` varchar(10000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rate` float DEFAULT NULL,
  `is_anonymous` tinyint(1) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `order_id` int(11) DEFAULT NULL,
  `is_re_comment` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `item_id` (`item_id`),
  KEY `user_id` (`user_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `item_comment_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),
  CONSTRAINT `item_comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `item_comment_ibfk_3` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_comment`
--

LOCK TABLES `item_comment` WRITE;
/*!40000 ALTER TABLE `item_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `item_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_fav`
--

DROP TABLE IF EXISTS `item_fav`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item_fav` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`item_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `item_fav_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),
  CONSTRAINT `item_fav_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_fav`
--

LOCK TABLES `item_fav` WRITE;
/*!40000 ALTER TABLE `item_fav` DISABLE KEYS */;
INSERT INTO `item_fav` VALUES (1,16,14,'2015-11-30 22:47:07'),(2,13,12,'2015-11-30 22:47:55'),(3,9,12,'2015-11-30 22:49:13'),(4,18,1,'2015-12-01 14:44:59'),(5,8,16,'2015-12-01 15:39:04'),(6,6,2,'2015-12-01 19:06:28');
/*!40000 ALTER TABLE `item_fav` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_sub_cat`
--

DROP TABLE IF EXISTS `item_sub_cat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item_sub_cat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `desc` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `icon` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cat_id` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cat_id` (`cat_id`),
  CONSTRAINT `item_sub_cat_ibfk_1` FOREIGN KEY (`cat_id`) REFERENCES `item_cat` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_sub_cat`
--

LOCK TABLES `item_sub_cat` WRITE;
/*!40000 ALTER TABLE `item_sub_cat` DISABLE KEYS */;
INSERT INTO `item_sub_cat` VALUES (1,'祛斑','','subcaticon/1448868808.48',1,1),(2,'点痣','','subcaticon/1448868716.87',1,1),(3,'祛痘','','subcaticon/1448868685.91',1,1),(4,'嫩肤','','subcaticon/1448868670.32',1,1),(5,'双眼皮','','subcaticon/1448868653.71',2,1),(6,'开眼角','','subcaticon/1448868641.63',2,1),(7,'去眼袋','','subcaticon/1448868629.15',2,1),(8,'隆鼻','','subcaticon/1448868616.87',3,1),(9,'脱毛','','subcaticon/1448868599.35',4,1),(10,'玻尿酸','','subcaticon/1448868528.36',5,1),(11,'肉毒素','','subcaticon/1448868544.83',5,1),(12,'洗牙','','subcaticon/1448883145.29',6,1),(13,'牙齿美白','','subcaticon/1448890154.66',6,1);
/*!40000 ALTER TABLE `item_sub_cat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pay_method` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `order_no` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `credit_choice_id` int(11) DEFAULT NULL,
  `coupon_id` int(11) DEFAULT NULL,
  `coupon_amount` decimal(10,2) NOT NULL,
  `credit_amount` decimal(10,2) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `create_time` datetime DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `credit_verified` tinyint(1) NOT NULL,
  `hospital_id` int(11) NOT NULL,
  `transaction_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `refund` tinyint(1) NOT NULL,
  `user_finished` tinyint(1) DEFAULT NULL,
  `total_fee` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `coupon_id` (`coupon_id`),
  UNIQUE KEY `order_no` (`order_no`),
  KEY `credit_choice_id` (`credit_choice_id`),
  KEY `item_id` (`item_id`),
  KEY `user_id` (`user_id`),
  KEY `hospital_id` (`hospital_id`),
  CONSTRAINT `order_ibfk_1` FOREIGN KEY (`coupon_id`) REFERENCES `user_coupon` (`id`),
  CONSTRAINT `order_ibfk_2` FOREIGN KEY (`credit_choice_id`) REFERENCES `period_pay_choice` (`id`),
  CONSTRAINT `order_ibfk_3` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),
  CONSTRAINT `order_ibfk_4` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `order_ibfk_5` FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (20,0,2,6,'201512021016661129510905',NULL,11,100.00,0.00,200.00,300.00,'2015-12-02 10:16:30',10,1,3,NULL,0,0,0.00),(21,0,2,6,'201512021018068456886993',NULL,10,100.00,0.00,200.00,300.00,'2015-12-02 10:18:57',10,1,3,NULL,1,0,0.00),(22,0,11,6,'201512021259242954177086',NULL,NULL,0.00,0.00,300.00,300.00,'2015-12-02 12:59:54',10,1,3,NULL,1,0,0.00),(23,0,11,6,'201512021301906104610035',NULL,NULL,0.00,0.00,300.00,300.00,'2015-12-02 13:01:05',10,1,3,NULL,1,0,0.00),(24,0,11,6,'201512021306561540575534',NULL,NULL,0.00,0.00,300.00,300.00,'2015-12-02 13:06:41',10,1,3,'1009870821201512021865719675',1,0,0.00),(25,0,11,6,'201512021309116459106184',NULL,NULL,0.00,0.00,300.00,300.00,'2015-12-02 13:09:59',10,1,3,'1009870821201512021865770982',1,0,0.00),(26,0,11,6,'201512021428013736555494',NULL,NULL,0.00,0.00,1.00,1.00,'2015-12-02 14:28:37',7,1,3,'1009870821201512021866943691',1,0,0.00),(27,0,1,7,'201512021438026402687482',NULL,24,100.00,0.00,780.00,880.00,'2015-12-02 14:38:03',0,1,2,NULL,0,0,0.00),(28,0,1,7,'201512021440707545714956',NULL,21,100.00,0.00,780.00,880.00,'2015-12-02 14:40:46',0,1,2,NULL,0,0,0.00),(29,0,21,6,'201512021441125951759786',NULL,NULL,0.00,0.00,300.00,300.00,'2015-12-02 14:41:52',7,1,3,'1009870821201512021867126690',1,0,0.00);
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_log`
--

DROP TABLE IF EXISTS `order_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `remark` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `order_log_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_log`
--

LOCK TABLES `order_log` WRITE;
/*!40000 ALTER TABLE `order_log` DISABLE KEYS */;
INSERT INTO `order_log` VALUES (5,20,10,NULL,'2015-12-02 10:18:33'),(6,21,10,NULL,'2015-12-02 10:19:20'),(7,23,10,NULL,'2015-12-02 13:03:19'),(8,22,10,NULL,'2015-12-02 13:03:28'),(9,25,7,NULL,'2015-12-02 13:11:30'),(10,26,7,NULL,'2015-12-02 14:29:22'),(11,29,7,NULL,'2015-12-02 14:42:31');
/*!40000 ALTER TABLE `order_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pay_log_order_no`
--

DROP TABLE IF EXISTS `pay_log_order_no`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pay_log_order_no` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_no` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `period_pay_log_id` int(11) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `create_time` datetime DEFAULT NULL,
  `total` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `period_pay_log_id` (`period_pay_log_id`),
  KEY `ix_pay_log_order_no_order_no` (`order_no`),
  CONSTRAINT `pay_log_order_no_ibfk_1` FOREIGN KEY (`period_pay_log_id`) REFERENCES `period_pay_log` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pay_log_order_no`
--

LOCK TABLES `pay_log_order_no` WRITE;
/*!40000 ALTER TABLE `pay_log_order_no` DISABLE KEYS */;
/*!40000 ALTER TABLE `pay_log_order_no` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pay_notify_log`
--

DROP TABLE IF EXISTS `pay_notify_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pay_notify_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pay_type` tinyint(1) NOT NULL,
  `content` varchar(10000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pay_notify_log`
--

LOCK TABLES `pay_notify_log` WRITE;
/*!40000 ALTER TABLE `pay_notify_log` DISABLE KEYS */;
INSERT INTO `pay_notify_log` VALUES (1,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[CFT]]></bank_type>\n<cash_fee><![CDATA[1]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[6wdce5dj47go8klffwvm31afmaiexev6]]></nonce_str>\n<openid><![CDATA[o56qvw9XQZ2-JATmeVcdMNveGJzk]]></openid>\n<out_trade_no><![CDATA[201511301622582259003125]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[C3CD2CD93F3AAE2855998877E2B6F8A8]]></sign>\n<time_end><![CDATA[20151130162309]]></time_end>\n<total_fee>1</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1002960821201511301837248823]]></transaction_id>\n</xml>','2015-11-30 16:23:10'),(2,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[CFT]]></bank_type>\n<cash_fee><![CDATA[1]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[p8owb1f9vcx3roeo3k011trh347ja15b]]></nonce_str>\n<openid><![CDATA[o56qvw9XQZ2-JATmeVcdMNveGJzk]]></openid>\n<out_trade_no><![CDATA[201511301627255817210882]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[1CD85FDE493E20C01F746E3D731D54E9]]></sign>\n<time_end><![CDATA[20151130162727]]></time_end>\n<total_fee>1</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1002960821201511301837299679]]></transaction_id>\n</xml>','2015-11-30 16:27:29'),(3,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[CFT]]></bank_type>\n<cash_fee><![CDATA[1]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[y7rl7j0a129kjif6lmi61kteth57ciow]]></nonce_str>\n<openid><![CDATA[o56qvw-ThtwfthGGlZ-XbH-3fjRc]]></openid>\n<out_trade_no><![CDATA[201511301629100232223211]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[C9FBA9AD7C1746987914BAB54DBDFFFB]]></sign>\n<time_end><![CDATA[20151130162939]]></time_end>\n<total_fee>1</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1006420821201511301837332260]]></transaction_id>\n</xml>','2015-11-30 16:29:40'),(4,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[CFT]]></bank_type>\n<cash_fee><![CDATA[1]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[nts6jttek9uj7sy4x22yxu54waff59pm]]></nonce_str>\n<openid><![CDATA[o56qvw9XQZ2-JATmeVcdMNveGJzk]]></openid>\n<out_trade_no><![CDATA[201511302201813001452466]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[80BBCF9FBBCC0BE15D22A0692D6C2017]]></sign>\n<time_end><![CDATA[20151130220110]]></time_end>\n<total_fee>1</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1002960821201511301842764633]]></transaction_id>\n</xml>','2015-11-30 22:01:11'),(5,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[CFT]]></bank_type>\n<cash_fee><![CDATA[1]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[pakd4mtsug60e4ogb6fypyegi28ocjf8]]></nonce_str>\n<openid><![CDATA[o56qvw-ThtwfthGGlZ-XbH-3fjRc]]></openid>\n<out_trade_no><![CDATA[201511302209878036189303]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[C25947764F2B3129C8D59EAE145F6702]]></sign>\n<time_end><![CDATA[20151130220942]]></time_end>\n<total_fee>1</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1006420821201511301842875687]]></transaction_id>\n</xml>','2015-11-30 22:09:43'),(6,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[ICBC_CREDIT]]></bank_type>\n<cash_fee><![CDATA[30000]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[85m0daqcswbzkl4z15pw0eyfzdcigxbf]]></nonce_str>\n<openid><![CDATA[o56qvwxvcD7ddq1GoEr0XNyVAyYs]]></openid>\n<out_trade_no><![CDATA[201512021301906104610035]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[8881AC2C65C349B084B7E7B68E1D07BA]]></sign>\n<time_end><![CDATA[20151202130118]]></time_end>\n<total_fee>30000</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1009870821201512021865617949]]></transaction_id>\n</xml>','2015-12-02 13:01:20'),(7,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[ICBC_CREDIT]]></bank_type>\n<cash_fee><![CDATA[30000]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[85m0daqcswbzkl4z15pw0eyfzdcigxbf]]></nonce_str>\n<openid><![CDATA[o56qvwxvcD7ddq1GoEr0XNyVAyYs]]></openid>\n<out_trade_no><![CDATA[201512021301906104610035]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[8881AC2C65C349B084B7E7B68E1D07BA]]></sign>\n<time_end><![CDATA[20151202130118]]></time_end>\n<total_fee>30000</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1009870821201512021865617949]]></transaction_id>\n</xml>','2015-12-02 13:01:29'),(8,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[ICBC_CREDIT]]></bank_type>\n<cash_fee><![CDATA[30000]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[85m0daqcswbzkl4z15pw0eyfzdcigxbf]]></nonce_str>\n<openid><![CDATA[o56qvwxvcD7ddq1GoEr0XNyVAyYs]]></openid>\n<out_trade_no><![CDATA[201512021301906104610035]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[8881AC2C65C349B084B7E7B68E1D07BA]]></sign>\n<time_end><![CDATA[20151202130118]]></time_end>\n<total_fee>30000</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1009870821201512021865617949]]></transaction_id>\n</xml>','2015-12-02 13:01:48'),(9,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[ICBC_CREDIT]]></bank_type>\n<cash_fee><![CDATA[30000]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[85m0daqcswbzkl4z15pw0eyfzdcigxbf]]></nonce_str>\n<openid><![CDATA[o56qvwxvcD7ddq1GoEr0XNyVAyYs]]></openid>\n<out_trade_no><![CDATA[201512021301906104610035]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[8881AC2C65C349B084B7E7B68E1D07BA]]></sign>\n<time_end><![CDATA[20151202130118]]></time_end>\n<total_fee>30000</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1009870821201512021865617949]]></transaction_id>\n</xml>','2015-12-02 13:02:20'),(10,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[ICBC_CREDIT]]></bank_type>\n<cash_fee><![CDATA[30000]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[85m0daqcswbzkl4z15pw0eyfzdcigxbf]]></nonce_str>\n<openid><![CDATA[o56qvwxvcD7ddq1GoEr0XNyVAyYs]]></openid>\n<out_trade_no><![CDATA[201512021301906104610035]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[8881AC2C65C349B084B7E7B68E1D07BA]]></sign>\n<time_end><![CDATA[20151202130118]]></time_end>\n<total_fee>30000</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1009870821201512021865617949]]></transaction_id>\n</xml>','2015-12-02 13:05:21'),(11,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[ICBC_CREDIT]]></bank_type>\n<cash_fee><![CDATA[30000]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[trsi0cypp3j39dtz63kmvwi1vq7hgc6g]]></nonce_str>\n<openid><![CDATA[o56qvwxvcD7ddq1GoEr0XNyVAyYs]]></openid>\n<out_trade_no><![CDATA[201512021306561540575534]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[D07FF3BBA26CBDBEC956FC5873271308]]></sign>\n<time_end><![CDATA[20151202130647]]></time_end>\n<total_fee>30000</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1009870821201512021865719675]]></transaction_id>\n</xml>','2015-12-02 13:06:49'),(12,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[ICBC_CREDIT]]></bank_type>\n<cash_fee><![CDATA[30000]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[trsi0cypp3j39dtz63kmvwi1vq7hgc6g]]></nonce_str>\n<openid><![CDATA[o56qvwxvcD7ddq1GoEr0XNyVAyYs]]></openid>\n<out_trade_no><![CDATA[201512021306561540575534]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[D07FF3BBA26CBDBEC956FC5873271308]]></sign>\n<time_end><![CDATA[20151202130647]]></time_end>\n<total_fee>30000</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1009870821201512021865719675]]></transaction_id>\n</xml>','2015-12-02 13:06:57'),(13,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[ICBC_CREDIT]]></bank_type>\n<cash_fee><![CDATA[30000]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[trsi0cypp3j39dtz63kmvwi1vq7hgc6g]]></nonce_str>\n<openid><![CDATA[o56qvwxvcD7ddq1GoEr0XNyVAyYs]]></openid>\n<out_trade_no><![CDATA[201512021306561540575534]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[D07FF3BBA26CBDBEC956FC5873271308]]></sign>\n<time_end><![CDATA[20151202130647]]></time_end>\n<total_fee>30000</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1009870821201512021865719675]]></transaction_id>\n</xml>','2015-12-02 13:07:13'),(14,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[ICBC_CREDIT]]></bank_type>\n<cash_fee><![CDATA[30000]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[trsi0cypp3j39dtz63kmvwi1vq7hgc6g]]></nonce_str>\n<openid><![CDATA[o56qvwxvcD7ddq1GoEr0XNyVAyYs]]></openid>\n<out_trade_no><![CDATA[201512021306561540575534]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[D07FF3BBA26CBDBEC956FC5873271308]]></sign>\n<time_end><![CDATA[20151202130647]]></time_end>\n<total_fee>30000</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1009870821201512021865719675]]></transaction_id>\n</xml>','2015-12-02 13:07:46'),(15,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[ICBC_CREDIT]]></bank_type>\n<cash_fee><![CDATA[30000]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[xmj7677u9r0bxy7ef54g14y83rw32p8d]]></nonce_str>\n<openid><![CDATA[o56qvwxvcD7ddq1GoEr0XNyVAyYs]]></openid>\n<out_trade_no><![CDATA[201512021309116459106184]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[5649B9E6666168D05B9EB127C6BE7C8E]]></sign>\n<time_end><![CDATA[20151202131011]]></time_end>\n<total_fee>30000</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1009870821201512021865770982]]></transaction_id>\n</xml>','2015-12-02 13:10:12'),(16,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[ICBC_CREDIT]]></bank_type>\n<cash_fee><![CDATA[30000]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[trsi0cypp3j39dtz63kmvwi1vq7hgc6g]]></nonce_str>\n<openid><![CDATA[o56qvwxvcD7ddq1GoEr0XNyVAyYs]]></openid>\n<out_trade_no><![CDATA[201512021306561540575534]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[D07FF3BBA26CBDBEC956FC5873271308]]></sign>\n<time_end><![CDATA[20151202130647]]></time_end>\n<total_fee>30000</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1009870821201512021865719675]]></transaction_id>\n</xml>','2015-12-02 13:10:47'),(17,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[ICBC_CREDIT]]></bank_type>\n<cash_fee><![CDATA[30000]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[85m0daqcswbzkl4z15pw0eyfzdcigxbf]]></nonce_str>\n<openid><![CDATA[o56qvwxvcD7ddq1GoEr0XNyVAyYs]]></openid>\n<out_trade_no><![CDATA[201512021301906104610035]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[8881AC2C65C349B084B7E7B68E1D07BA]]></sign>\n<time_end><![CDATA[20151202130118]]></time_end>\n<total_fee>30000</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1009870821201512021865617949]]></transaction_id>\n</xml>','2015-12-02 13:35:23'),(18,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[ICBC_CREDIT]]></bank_type>\n<cash_fee><![CDATA[100]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[Y]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[i55t9af9a1y6302grbfjcbr5q17oz82a]]></nonce_str>\n<openid><![CDATA[o56qvwxvcD7ddq1GoEr0XNyVAyYs]]></openid>\n<out_trade_no><![CDATA[201512021428013736555494]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[05C3A124C2D4D77F9A68154210DDEA03]]></sign>\n<time_end><![CDATA[20151202142850]]></time_end>\n<total_fee>100</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1009870821201512021866943691]]></transaction_id>\n</xml>','2015-12-02 14:28:51'),(19,1,'<xml><appid><![CDATA[wx284c24dbdca7b377]]></appid>\n<bank_type><![CDATA[ICBC_CREDIT]]></bank_type>\n<cash_fee><![CDATA[30000]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[N]]></is_subscribe>\n<mch_id><![CDATA[1278286901]]></mch_id>\n<nonce_str><![CDATA[ey5unjonj5xl7sbv00din230msayuog6]]></nonce_str>\n<openid><![CDATA[o56qvwxvcD7ddq1GoEr0XNyVAyYs]]></openid>\n<out_trade_no><![CDATA[201512021441125951759786]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[5980206773F7E2DF3509FD9DA55D2483]]></sign>\n<time_end><![CDATA[20151202144201]]></time_end>\n<total_fee>30000</total_fee>\n<trade_type><![CDATA[JSAPI]]></trade_type>\n<transaction_id><![CDATA[1009870821201512021867126690]]></transaction_id>\n</xml>','2015-12-02 14:42:02'),(20,1,'','2015-12-02 15:24:12'),(21,1,'','2015-12-02 16:23:07');
/*!40000 ALTER TABLE `pay_notify_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `period_pay_choice`
--

DROP TABLE IF EXISTS `period_pay_choice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `period_pay_choice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `period_count` int(11) NOT NULL,
  `period_fee` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `period_count` (`period_count`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `period_pay_choice`
--

LOCK TABLES `period_pay_choice` WRITE;
/*!40000 ALTER TABLE `period_pay_choice` DISABLE KEYS */;
INSERT INTO `period_pay_choice` VALUES (1,3,0.03),(2,6,0.05),(3,12,0.102),(5,18,0.153),(6,24,0.212);
/*!40000 ALTER TABLE `period_pay_choice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `period_pay_log`
--

DROP TABLE IF EXISTS `period_pay_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `period_pay_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` decimal(10,2) NOT NULL,
  `fee` decimal(10,2) NOT NULL,
  `punish` decimal(10,2) NOT NULL,
  `user_id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `period_pay_index` int(11) DEFAULT NULL,
  `period_count` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `deadline` datetime DEFAULT NULL,
  `repayment_time` datetime DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `period_pay_log_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`),
  CONSTRAINT `period_pay_log_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `period_pay_log`
--

LOCK TABLES `period_pay_log` WRITE;
/*!40000 ALTER TABLE `period_pay_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `period_pay_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `punish_log`
--

DROP TABLE IF EXISTS `punish_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `punish_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `log_id` int(11) DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `log_id` (`log_id`),
  CONSTRAINT `punish_log_ibfk_1` FOREIGN KEY (`log_id`) REFERENCES `period_pay_log` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `punish_log`
--

LOCK TABLES `punish_log` WRITE;
/*!40000 ALTER TABLE `punish_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `punish_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recommend_item`
--

DROP TABLE IF EXISTS `recommend_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recommend_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` int(11) DEFAULT NULL,
  `sort_order` int(11) DEFAULT NULL,
  `desc` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `item_id` (`item_id`),
  CONSTRAINT `recommend_item_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recommend_item`
--

LOCK TABLES `recommend_item` WRITE;
/*!40000 ALTER TABLE `recommend_item` DISABLE KEYS */;
INSERT INTO `recommend_item` VALUES (1,1,100,'该项目个性化设计，且损伤小、恢复快、易修复','subcaticon/1448865835.83'),(2,2,40,'该项目纯进口，安全，且效果立显，不影响工作学习','subcaticon/1448868936.11'),(3,5,60,'该项目为进口botox瘦脸针，安全见效快','subcaticon/1448941657.7'),(5,10,120,'该项目采用的硅胶假体与鼻腔相容性好，较少排异','subcaticon/1448941598.53'),(7,19,21,'该项目通过国际CFDA认证，安全放心','subcaticon/1448967430.36');
/*!40000 ALTER TABLE `recommend_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recommend_subcat`
--

DROP TABLE IF EXISTS `recommend_subcat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recommend_subcat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sub_cat_id` int(11) DEFAULT NULL,
  `sort_order` int(11) DEFAULT NULL,
  `icon` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sub_cat_id` (`sub_cat_id`),
  CONSTRAINT `recommend_subcat_ibfk_1` FOREIGN KEY (`sub_cat_id`) REFERENCES `item_sub_cat` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recommend_subcat`
--

LOCK TABLES `recommend_subcat` WRITE;
/*!40000 ALTER TABLE `recommend_subcat` DISABLE KEYS */;
INSERT INTO `recommend_subcat` VALUES (1,5,100,'subcaticon/1448853235.12'),(2,3,120,'subcaticon/1448853676.86'),(3,1,140,'subcaticon/1448853704.26'),(4,9,181,'subcaticon/1448853771.26'),(5,2,150,'subcaticon/1448853801.15'),(6,11,160,'subcaticon/1448853841.36'),(7,8,110,'subcaticon/1448853868.16'),(8,10,170,'subcaticon/1448868558.52'),(9,13,200,'subcaticon/1448947896.71');
/*!40000 ALTER TABLE `recommend_subcat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repayment`
--

DROP TABLE IF EXISTS `repayment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `repayment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `order_no` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `coupon_id` int(11) DEFAULT NULL,
  `pay_method` tinyint(1) NOT NULL,
  `transaction_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `data` varchar(10000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_no` (`order_no`),
  UNIQUE KEY `coupon_id` (`coupon_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `repayment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `repayment_ibfk_2` FOREIGN KEY (`coupon_id`) REFERENCES `user_coupon` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repayment`
--

LOCK TABLES `repayment` WRITE;
/*!40000 ALTER TABLE `repayment` DISABLE KEYS */;
INSERT INTO `repayment` VALUES (1,2,1050.00,'201511301626044655975140','2015-11-30 16:26:56','2015-11-30 16:26:56',0,NULL,0,NULL,'[{\"punish\": \"0\", \"amount\": \"1000\", \"fee\": \"50\", \"id\": \"1\"}]'),(2,2,2423.33,'201511301628934918751321','2015-11-30 16:28:19','2015-11-30 16:28:19',0,NULL,0,NULL,'[{\"punish\": \"0\", \"amount\": \"1000\", \"fee\": \"50\", \"id\": \"1\"}, {\"punish\": \"0\", \"amount\": \"1333.33\", \"fee\": \"40\", \"id\": \"7\"}]'),(3,2,2423.33,'201511301628922239991940','2015-11-30 16:28:40','2015-11-30 16:28:40',0,NULL,0,NULL,'[{\"punish\": \"0\", \"amount\": \"1000\", \"fee\": \"50\", \"id\": \"1\"}, {\"punish\": \"0\", \"amount\": \"1333.33\", \"fee\": \"40\", \"id\": \"7\"}]'),(4,2,2423.33,'201511301628062149242597','2015-11-30 16:28:49','2015-11-30 16:28:49',0,NULL,0,NULL,'[{\"punish\": \"0\", \"amount\": \"1000\", \"fee\": \"50\", \"id\": \"1\"}, {\"punish\": \"0\", \"amount\": \"1333.33\", \"fee\": \"40\", \"id\": \"7\"}]');
/*!40000 ALTER TABLE `repayment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school`
--

DROP TABLE IF EXISTS `school`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `city_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `link` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school`
--

LOCK TABLES `school` WRITE;
/*!40000 ALTER TABLE `school` DISABLE KEYS */;
/*!40000 ALTER TABLE `school` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_code`
--

DROP TABLE IF EXISTS `service_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `service_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) DEFAULT NULL,
  `code` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `create_time` datetime DEFAULT NULL,
  `book_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  UNIQUE KEY `ix_service_code_code` (`code`),
  CONSTRAINT `service_code_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_code`
--

LOCK TABLES `service_code` WRITE;
/*!40000 ALTER TABLE `service_code` DISABLE KEYS */;
INSERT INTO `service_code` VALUES (9,25,'urlie0',0,'2015-12-02 13:10:12',NULL),(10,24,'wc537z',0,'2015-12-02 13:10:47',NULL),(11,26,'je4hqi',0,'2015-12-02 14:28:51',NULL),(12,29,'mywsko',0,'2015-12-02 14:42:02',NULL);
/*!40000 ALTER TABLE `service_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `passwd` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avatar` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'xianpeng','18801794295','123456','avatar/1448878641.78'),(2,'我叫鲁鲁','18750552673','121212','avatar/1448890645.98'),(3,'h07sijundp','10000000001','123456',NULL),(4,'Thomas_Ding','13122022388','123456','avatar/1448889766.49'),(5,'lv1wr5fuqt','18721939373','fanhui811027',NULL),(7,'美分分为你加分','18621955395','111111',NULL),(8,'buun34yjxd','13564516057','chenjie5w',NULL),(9,'qrhqnbb9k1','18918800148','111111','avatar/1448886863.37'),(10,'u9avrxg0tu','18017076711','860927',NULL),(11,'cru8ja8rsy','18818057058','19820102',NULL),(12,'qfvf3gylzm','13148492169','111111','avatar/1448889605.65'),(13,'疯狂顽皮🐰','15502121025','','avatar/1448890889.35'),(14,'xhhzxfrqrg','18616977502','ivy366ss720520',NULL),(15,'muwptvestf','15800961787','15800961787wjh',NULL),(16,'pv5elidsje','18621871289','kikiku',NULL),(19,'hunsycnmeg','18977472781','wangyunyan2199','avatar/1448955986.14'),(20,'k4ebzrolxs','15026622775','moon105',NULL),(21,'qehq80ovzs','18001866011','19820102',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_advice`
--

DROP TABLE IF EXISTS `user_advice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_advice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `content` varchar(10000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contact` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_advice_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_advice`
--

LOCK TABLES `user_advice` WRITE;
/*!40000 ALTER TABLE `user_advice` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_advice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_coupon`
--

DROP TABLE IF EXISTS `user_coupon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_coupon` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `coupon_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `cat` tinyint(1) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `end_time` datetime NOT NULL,
  `create_time` datetime NOT NULL,
  `remark` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `coupon_id` (`coupon_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_coupon_ibfk_1` FOREIGN KEY (`coupon_id`) REFERENCES `coupon` (`id`),
  CONSTRAINT `user_coupon_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_coupon`
--

LOCK TABLES `user_coupon` WRITE;
/*!40000 ALTER TABLE `user_coupon` DISABLE KEYS */;
INSERT INTO `user_coupon` VALUES (1,1,2,0,100.00,0,'2015-12-30 17:57:51','2015-11-30 17:57:51',''),(2,1,2,0,100.00,0,'2015-12-30 17:57:53','2015-11-30 17:57:53',''),(3,1,2,0,100.00,0,'2015-12-30 17:57:54','2015-11-30 17:57:54',''),(4,1,2,0,100.00,0,'2015-12-30 17:58:02','2015-11-30 17:58:02',''),(5,1,2,0,100.00,0,'2015-12-30 17:58:02','2015-11-30 17:58:02',''),(6,1,2,0,100.00,0,'2015-12-30 17:58:02','2015-11-30 17:58:02',''),(7,1,2,0,100.00,0,'2015-12-30 17:58:02','2015-11-30 17:58:02',''),(8,1,2,0,100.00,0,'2015-12-30 17:58:02','2015-11-30 17:58:02',''),(9,1,2,0,100.00,0,'2015-12-30 17:58:02','2015-11-30 17:58:02',''),(10,1,2,0,100.00,1,'2015-12-30 17:58:02','2015-11-30 17:58:02',''),(11,1,2,0,100.00,1,'2015-12-30 17:58:02','2015-11-30 17:58:02',''),(12,1,2,0,100.00,1,'2015-12-30 17:58:02','2015-11-30 17:58:02',''),(13,1,2,0,100.00,1,'2015-12-30 17:58:02','2015-11-30 17:58:02',''),(14,1,1,0,100.00,1,'2015-12-30 18:20:21','2015-11-30 18:20:21',''),(15,1,1,0,100.00,1,'2015-12-30 18:20:26','2015-11-30 18:20:26',''),(16,1,1,0,100.00,1,'2015-12-30 18:20:26','2015-11-30 18:20:26',''),(17,1,1,0,100.00,1,'2015-12-30 18:20:26','2015-11-30 18:20:26',''),(18,1,1,0,100.00,1,'2015-12-30 18:20:26','2015-11-30 18:20:26',''),(19,1,1,0,100.00,1,'2015-12-30 18:20:26','2015-11-30 18:20:26',''),(20,1,1,0,100.00,0,'2015-12-30 18:20:26','2015-11-30 18:20:26',''),(21,1,1,0,100.00,1,'2015-12-30 18:20:26','2015-11-30 18:20:26',''),(22,1,1,0,100.00,1,'2015-12-30 18:20:26','2015-11-30 18:20:26',''),(23,1,1,0,100.00,1,'2015-12-30 18:20:26','2015-11-30 18:20:26',''),(24,1,1,0,100.00,1,'2015-12-30 18:20:26','2015-11-30 18:20:26',''),(25,1,4,0,100.00,0,'2015-12-31 18:56:53','2015-12-01 18:56:53','');
/*!40000 ALTER TABLE `user_coupon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_credit`
--

DROP TABLE IF EXISTS `user_credit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_credit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `used` decimal(10,2) NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_credit_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_credit`
--

LOCK TABLES `user_credit` WRITE;
/*!40000 ALTER TABLE `user_credit` DISABLE KEYS */;
INSERT INTO `user_credit` VALUES (37,1,10000.00,0.00,1),(38,2,600.00,0.00,2),(39,3,10000.00,0.00,0),(43,4,10000.00,0.00,2),(44,5,10000.00,0.00,0),(50,7,10000.00,0.00,0),(53,8,10000.00,0.00,0),(64,9,10000.00,0.00,0),(65,11,10000.00,0.00,0),(66,12,10000.00,0.00,0),(67,10,10000.00,0.00,0),(68,13,10000.00,0.00,0),(69,14,10000.00,0.00,0),(70,15,10000.00,0.00,0),(71,16,10000.00,0.00,0),(72,19,10000.00,0.00,0),(73,20,10000.00,0.00,0),(74,21,10000.00,0.00,0);
/*!40000 ALTER TABLE `user_credit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wechat`
--

DROP TABLE IF EXISTS `wechat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wechat` (
  `open_id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`open_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `wechat_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wechat`
--

LOCK TABLES `wechat` WRITE;
/*!40000 ALTER TABLE `wechat` DISABLE KEYS */;
INSERT INTO `wechat` VALUES ('o56qvw-ThtwfthGGlZ-XbH-3fjRc',NULL,'2015-12-01 01:28:26',0),('o56qvw7Xd7UDuRa-yN1JV5pGIMS0',NULL,'2015-12-01 06:04:33',0),('o56qvwxvcD7ddq1GoEr0XNyVAyYs',NULL,'2015-12-02 12:59:55',0),('o56qvwzPLG5qXXzn00KQbr6IisVk',NULL,'2015-12-01 15:46:52',0);
/*!40000 ALTER TABLE `wechat` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-12-02 16:46:56
