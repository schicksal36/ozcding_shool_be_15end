-- MySQL dump 10.13  Distrib 8.4.7, for Win64 (x86_64)
--
-- Host: localhost    Database: bookmark
-- ------------------------------------------------------
-- Server version	8.4.7

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add 북마크',7,'add_bookmark'),(26,'Can change 북마크',7,'change_bookmark'),(27,'Can delete 북마크',7,'delete_bookmark'),(28,'Can view 북마크',7,'view_bookmark');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1200000$87uKz7y7vmZ5SXl3PpbEoP$kZ2yuHlImyfm4KcYpJD2OvAc2tzCVGPCpEzqkgDKwRU=','2025-12-15 02:09:25.395634',1,'schicksal36','','','',1,1,'2025-12-13 14:58:38.390087');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookmark_bookmark`
--

DROP TABLE IF EXISTS `bookmark_bookmark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookmark_bookmark` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=203 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookmark_bookmark`
--

LOCK TABLES `bookmark_bookmark` WRITE;
/*!40000 ALTER TABLE `bookmark_bookmark` DISABLE KEYS */;
INSERT INTO `bookmark_bookmark` VALUES (1,'구글','https://www.google.com','2025-12-13 15:19:07.655689','2025-12-13 15:19:22.405927'),(2,'네이버','https://WWW.NAVER.COM','2025-12-13 15:19:48.511158','2025-12-13 15:19:48.511178'),(3,'test_naver0','htts://naver.com','2025-12-14 13:07:11.004076','2025-12-14 13:07:11.004122'),(4,'test_naver1','htts://naver.com','2025-12-14 13:07:11.030133','2025-12-14 13:07:11.030159'),(5,'test_naver2','htts://naver.com','2025-12-14 13:07:11.033845','2025-12-14 13:07:11.033875'),(6,'test_naver3','htts://naver.com','2025-12-14 13:07:11.037448','2025-12-14 13:07:11.037474'),(7,'test_naver4','htts://naver.com','2025-12-14 13:07:11.041182','2025-12-14 13:07:11.041207'),(8,'test_naver5','htts://naver.com','2025-12-14 13:07:11.044360','2025-12-14 13:07:11.044383'),(9,'test_naver6','htts://naver.com','2025-12-14 13:07:11.047616','2025-12-14 13:07:11.047641'),(10,'test_naver7','htts://naver.com','2025-12-14 13:07:11.052104','2025-12-14 13:07:11.052131'),(11,'test_naver8','htts://naver.com','2025-12-14 13:07:11.057962','2025-12-14 13:07:11.057990'),(12,'test_naver9','htts://naver.com','2025-12-14 13:07:11.062626','2025-12-14 13:07:11.062651'),(13,'test_naver10','htts://naver.com','2025-12-14 13:07:11.066712','2025-12-14 13:07:11.066739'),(14,'test_naver11','htts://naver.com','2025-12-14 13:07:11.070172','2025-12-14 13:07:11.070198'),(15,'test_naver12','htts://naver.com','2025-12-14 13:07:11.073035','2025-12-14 13:07:11.073057'),(16,'test_naver13','htts://naver.com','2025-12-14 13:07:11.076218','2025-12-14 13:07:11.076257'),(17,'test_naver14','htts://naver.com','2025-12-14 13:07:11.079073','2025-12-14 13:07:11.079095'),(18,'test_naver15','htts://naver.com','2025-12-14 13:07:11.082001','2025-12-14 13:07:11.082023'),(19,'test_naver16','htts://naver.com','2025-12-14 13:07:11.084844','2025-12-14 13:07:11.084867'),(20,'test_naver17','htts://naver.com','2025-12-14 13:07:11.088014','2025-12-14 13:07:11.088039'),(21,'test_naver18','htts://naver.com','2025-12-14 13:07:11.090959','2025-12-14 13:07:11.090983'),(22,'test_naver19','htts://naver.com','2025-12-14 13:07:11.094197','2025-12-14 13:07:11.094223'),(23,'test_naver20','htts://naver.com','2025-12-14 13:07:11.097035','2025-12-14 13:07:11.097058'),(24,'test_naver21','htts://naver.com','2025-12-14 13:07:11.099807','2025-12-14 13:07:11.099829'),(25,'test_naver22','htts://naver.com','2025-12-14 13:07:11.103280','2025-12-14 13:07:11.103304'),(26,'test_naver23','htts://naver.com','2025-12-14 13:07:11.106048','2025-12-14 13:07:11.106071'),(27,'test_naver24','htts://naver.com','2025-12-14 13:07:11.109377','2025-12-14 13:07:11.109399'),(28,'test_naver25','htts://naver.com','2025-12-14 13:07:11.112576','2025-12-14 13:07:11.112604'),(29,'test_naver26','htts://naver.com','2025-12-14 13:07:11.116221','2025-12-14 13:07:11.116246'),(30,'test_naver27','htts://naver.com','2025-12-14 13:07:11.120381','2025-12-14 13:07:11.120421'),(31,'test_naver28','htts://naver.com','2025-12-14 13:07:11.124506','2025-12-14 13:07:11.124532'),(32,'test_naver29','htts://naver.com','2025-12-14 13:07:11.128192','2025-12-14 13:07:11.128217'),(33,'test_naver30','htts://naver.com','2025-12-14 13:07:11.132957','2025-12-14 13:07:11.132982'),(34,'test_naver31','htts://naver.com','2025-12-14 13:07:11.136229','2025-12-14 13:07:11.136255'),(35,'test_naver32','htts://naver.com','2025-12-14 13:07:11.139227','2025-12-14 13:07:11.139253'),(36,'test_naver33','htts://naver.com','2025-12-14 13:07:11.143192','2025-12-14 13:07:11.143216'),(37,'test_naver34','htts://naver.com','2025-12-14 13:07:11.148229','2025-12-14 13:07:11.148255'),(38,'test_naver35','htts://naver.com','2025-12-14 13:07:11.152213','2025-12-14 13:07:11.152238'),(39,'test_naver36','htts://naver.com','2025-12-14 13:07:11.155470','2025-12-14 13:07:11.155496'),(40,'test_naver37','htts://naver.com','2025-12-14 13:07:11.159305','2025-12-14 13:07:11.159330'),(41,'test_naver38','htts://naver.com','2025-12-14 13:07:11.163040','2025-12-14 13:07:11.163067'),(42,'test_naver39','htts://naver.com','2025-12-14 13:07:11.166651','2025-12-14 13:07:11.166680'),(43,'test_naver40','htts://naver.com','2025-12-14 13:07:11.170468','2025-12-14 13:07:11.170494'),(44,'test_naver41','htts://naver.com','2025-12-14 13:07:11.174413','2025-12-14 13:07:11.174440'),(45,'test_naver42','htts://naver.com','2025-12-14 13:07:11.178355','2025-12-14 13:07:11.178382'),(46,'test_naver43','htts://naver.com','2025-12-14 13:07:11.182276','2025-12-14 13:07:11.182310'),(47,'test_naver44','htts://naver.com','2025-12-14 13:07:11.186234','2025-12-14 13:07:11.186259'),(48,'test_naver45','htts://naver.com','2025-12-14 13:07:11.189874','2025-12-14 13:07:11.189900'),(49,'test_naver46','htts://naver.com','2025-12-14 13:07:11.193573','2025-12-14 13:07:11.193599'),(50,'test_naver47','htts://naver.com','2025-12-14 13:07:11.197675','2025-12-14 13:07:11.197718'),(51,'test_naver48','htts://naver.com','2025-12-14 13:07:11.201871','2025-12-14 13:07:11.201897'),(52,'test_naver49','htts://naver.com','2025-12-14 13:07:11.205937','2025-12-14 13:07:11.205963'),(53,'test_naver50','htts://naver.com','2025-12-14 13:07:11.209795','2025-12-14 13:07:11.209820'),(54,'test_naver51','htts://naver.com','2025-12-14 13:07:11.213176','2025-12-14 13:07:11.213203'),(55,'test_naver52','htts://naver.com','2025-12-14 13:07:11.216725','2025-12-14 13:07:11.216754'),(56,'test_naver53','htts://naver.com','2025-12-14 13:07:11.220823','2025-12-14 13:07:11.220850'),(57,'test_naver54','htts://naver.com','2025-12-14 13:07:11.228851','2025-12-14 13:07:11.228905'),(58,'test_naver55','htts://naver.com','2025-12-14 13:07:11.232546','2025-12-14 13:07:11.232573'),(59,'test_naver56','htts://naver.com','2025-12-14 13:07:11.236715','2025-12-14 13:07:11.236742'),(60,'test_naver57','htts://naver.com','2025-12-14 13:07:11.240517','2025-12-14 13:07:11.240542'),(61,'test_naver58','htts://naver.com','2025-12-14 13:07:11.244056','2025-12-14 13:07:11.244083'),(62,'test_naver59','htts://naver.com','2025-12-14 13:07:11.247870','2025-12-14 13:07:11.247897'),(63,'test_naver60','htts://naver.com','2025-12-14 13:07:11.252100','2025-12-14 13:07:11.252128'),(64,'test_naver61','htts://naver.com','2025-12-14 13:07:11.255545','2025-12-14 13:07:11.255572'),(65,'test_naver62','htts://naver.com','2025-12-14 13:07:11.259482','2025-12-14 13:07:11.259509'),(66,'test_naver63','htts://naver.com','2025-12-14 13:07:11.263300','2025-12-14 13:07:11.263328'),(67,'test_naver64','htts://naver.com','2025-12-14 13:07:11.266934','2025-12-14 13:07:11.266974'),(68,'test_naver65','htts://naver.com','2025-12-14 13:07:11.270853','2025-12-14 13:07:11.270881'),(69,'test_naver66','htts://naver.com','2025-12-14 13:07:11.274813','2025-12-14 13:07:11.274840'),(70,'test_naver67','htts://naver.com','2025-12-14 13:07:11.278589','2025-12-14 13:07:11.278615'),(71,'test_naver68','htts://naver.com','2025-12-14 13:07:11.282389','2025-12-14 13:07:11.282418'),(72,'test_naver69','htts://naver.com','2025-12-14 13:07:11.286289','2025-12-14 13:07:11.286316'),(73,'test_naver70','htts://naver.com','2025-12-14 13:07:11.290218','2025-12-14 13:07:11.290259'),(74,'test_naver71','htts://naver.com','2025-12-14 13:07:11.293965','2025-12-14 13:07:11.293994'),(75,'test_naver72','htts://naver.com','2025-12-14 13:07:11.297665','2025-12-14 13:07:11.297691'),(76,'test_naver73','htts://naver.com','2025-12-14 13:07:11.301100','2025-12-14 13:07:11.301127'),(77,'test_naver74','htts://naver.com','2025-12-14 13:07:11.304445','2025-12-14 13:07:11.304472'),(78,'test_naver75','htts://naver.com','2025-12-14 13:07:11.307832','2025-12-14 13:07:11.307860'),(79,'test_naver76','htts://naver.com','2025-12-14 13:07:11.311590','2025-12-14 13:07:11.311615'),(80,'test_naver77','htts://naver.com','2025-12-14 13:07:11.314954','2025-12-14 13:07:11.314981'),(81,'test_naver78','htts://naver.com','2025-12-14 13:07:11.318795','2025-12-14 13:07:11.318822'),(82,'test_naver79','htts://naver.com','2025-12-14 13:07:11.322094','2025-12-14 13:07:11.322121'),(83,'test_naver80','htts://naver.com','2025-12-14 13:07:11.325516','2025-12-14 13:07:11.325541'),(84,'test_naver81','htts://naver.com','2025-12-14 13:07:11.329422','2025-12-14 13:07:11.329448'),(85,'test_naver82','htts://naver.com','2025-12-14 13:07:11.333221','2025-12-14 13:07:11.333247'),(86,'test_naver83','htts://naver.com','2025-12-14 13:07:11.336787','2025-12-14 13:07:11.336814'),(87,'test_naver84','htts://naver.com','2025-12-14 13:07:11.340519','2025-12-14 13:07:11.340544'),(88,'test_naver85','htts://naver.com','2025-12-14 13:07:11.343425','2025-12-14 13:07:11.343447'),(89,'test_naver86','htts://naver.com','2025-12-14 13:07:11.346367','2025-12-14 13:07:11.346393'),(90,'test_naver87','htts://naver.com','2025-12-14 13:07:11.349970','2025-12-14 13:07:11.349996'),(91,'test_naver88','htts://naver.com','2025-12-14 13:07:11.354202','2025-12-14 13:07:11.354235'),(92,'test_naver89','htts://naver.com','2025-12-14 13:07:11.357724','2025-12-14 13:07:11.357750'),(93,'test_naver90','htts://naver.com','2025-12-14 13:07:11.361530','2025-12-14 13:07:11.361557'),(94,'test_naver91','htts://naver.com','2025-12-14 13:07:11.365306','2025-12-14 13:07:11.365332'),(95,'test_naver92','htts://naver.com','2025-12-14 13:07:11.368998','2025-12-14 13:07:11.369024'),(96,'test_naver93','htts://naver.com','2025-12-14 13:07:11.372646','2025-12-14 13:07:11.372672'),(97,'test_naver94','htts://naver.com','2025-12-14 13:07:11.376445','2025-12-14 13:07:11.376471'),(98,'test_naver95','htts://naver.com','2025-12-14 13:07:11.380156','2025-12-14 13:07:11.380182'),(99,'test_naver96','htts://naver.com','2025-12-14 13:07:11.383890','2025-12-14 13:07:11.383915'),(100,'test_naver97','htts://naver.com','2025-12-14 13:07:11.387597','2025-12-14 13:07:11.387623'),(101,'test_naver98','htts://naver.com','2025-12-14 13:07:11.391279','2025-12-14 13:07:11.391306'),(102,'test_naver99','htts://naver.com','2025-12-14 13:07:11.394986','2025-12-14 13:07:11.395011'),(103,'test 구글 0','https://google.com','2025-12-15 02:39:27.862810','2025-12-15 02:39:27.863632'),(104,'test 구글 1','https://google.com','2025-12-15 02:39:27.862862','2025-12-15 02:39:27.863641'),(105,'test 구글 2','https://google.com','2025-12-15 02:39:27.862880','2025-12-15 02:39:27.863649'),(106,'test 구글 3','https://google.com','2025-12-15 02:39:27.862891','2025-12-15 02:39:27.863657'),(107,'test 구글 4','https://google.com','2025-12-15 02:39:27.862900','2025-12-15 02:39:27.863665'),(108,'test 구글 5','https://google.com','2025-12-15 02:39:27.862909','2025-12-15 02:39:27.863673'),(109,'test 구글 6','https://google.com','2025-12-15 02:39:27.862918','2025-12-15 02:39:27.863681'),(110,'test 구글 7','https://google.com','2025-12-15 02:39:27.862926','2025-12-15 02:39:27.863689'),(111,'test 구글 8','https://google.com','2025-12-15 02:39:27.862934','2025-12-15 02:39:27.863697'),(112,'test 구글 9','https://google.com','2025-12-15 02:39:27.862943','2025-12-15 02:39:27.863705'),(113,'test 구글 10','https://google.com','2025-12-15 02:39:27.862951','2025-12-15 02:39:27.863713'),(114,'test 구글 11','https://google.com','2025-12-15 02:39:27.862959','2025-12-15 02:39:27.863720'),(115,'test 구글 12','https://google.com','2025-12-15 02:39:27.862967','2025-12-15 02:39:27.863728'),(116,'test 구글 13','https://google.com','2025-12-15 02:39:27.862975','2025-12-15 02:39:27.863736'),(117,'test 구글 14','https://google.com','2025-12-15 02:39:27.862983','2025-12-15 02:39:27.863744'),(118,'test 구글 15','https://google.com','2025-12-15 02:39:27.862991','2025-12-15 02:39:27.863751'),(119,'test 구글 16','https://google.com','2025-12-15 02:39:27.862998','2025-12-15 02:39:27.863759'),(120,'test 구글 17','https://google.com','2025-12-15 02:39:27.863005','2025-12-15 02:39:27.863767'),(121,'test 구글 18','https://google.com','2025-12-15 02:39:27.863013','2025-12-15 02:39:27.863775'),(122,'test 구글 19','https://google.com','2025-12-15 02:39:27.863020','2025-12-15 02:39:27.863783'),(123,'test 구글 20','https://google.com','2025-12-15 02:39:27.863028','2025-12-15 02:39:27.863790'),(124,'test 구글 21','https://google.com','2025-12-15 02:39:27.863036','2025-12-15 02:39:27.863798'),(125,'test 구글 22','https://google.com','2025-12-15 02:39:27.863043','2025-12-15 02:39:27.863805'),(126,'test 구글 23','https://google.com','2025-12-15 02:39:27.863051','2025-12-15 02:39:27.863813'),(127,'test 구글 24','https://google.com','2025-12-15 02:39:27.863058','2025-12-15 02:39:27.863820'),(128,'test 구글 25','https://google.com','2025-12-15 02:39:27.863066','2025-12-15 02:39:27.863827'),(129,'test 구글 26','https://google.com','2025-12-15 02:39:27.863073','2025-12-15 02:39:27.863835'),(130,'test 구글 27','https://google.com','2025-12-15 02:39:27.863081','2025-12-15 02:39:27.863842'),(131,'test 구글 28','https://google.com','2025-12-15 02:39:27.863089','2025-12-15 02:39:27.863849'),(132,'test 구글 29','https://google.com','2025-12-15 02:39:27.863096','2025-12-15 02:39:27.863857'),(133,'test 구글 30','https://google.com','2025-12-15 02:39:27.863103','2025-12-15 02:39:27.863864'),(134,'test 구글 31','https://google.com','2025-12-15 02:39:27.863111','2025-12-15 02:39:27.863871'),(135,'test 구글 32','https://google.com','2025-12-15 02:39:27.863118','2025-12-15 02:39:27.863897'),(136,'test 구글 33','https://google.com','2025-12-15 02:39:27.863126','2025-12-15 02:39:27.863906'),(137,'test 구글 34','https://google.com','2025-12-15 02:39:27.863134','2025-12-15 02:39:27.863913'),(138,'test 구글 35','https://google.com','2025-12-15 02:39:27.863141','2025-12-15 02:39:27.863921'),(139,'test 구글 36','https://google.com','2025-12-15 02:39:27.863149','2025-12-15 02:39:27.863928'),(140,'test 구글 37','https://google.com','2025-12-15 02:39:27.863156','2025-12-15 02:39:27.863935'),(141,'test 구글 38','https://google.com','2025-12-15 02:39:27.863164','2025-12-15 02:39:27.863943'),(142,'test 구글 39','https://google.com','2025-12-15 02:39:27.863171','2025-12-15 02:39:27.863950'),(143,'test 구글 40','https://google.com','2025-12-15 02:39:27.863178','2025-12-15 02:39:27.863958'),(144,'test 구글 41','https://google.com','2025-12-15 02:39:27.863186','2025-12-15 02:39:27.863965'),(145,'test 구글 42','https://google.com','2025-12-15 02:39:27.863193','2025-12-15 02:39:27.863973'),(146,'test 구글 43','https://google.com','2025-12-15 02:39:27.863201','2025-12-15 02:39:27.863980'),(147,'test 구글 44','https://google.com','2025-12-15 02:39:27.863208','2025-12-15 02:39:27.863987'),(148,'test 구글 45','https://google.com','2025-12-15 02:39:27.863216','2025-12-15 02:39:27.863995'),(149,'test 구글 46','https://google.com','2025-12-15 02:39:27.863223','2025-12-15 02:39:27.864002'),(150,'test 구글 47','https://google.com','2025-12-15 02:39:27.863231','2025-12-15 02:39:27.864009'),(151,'test 구글 48','https://google.com','2025-12-15 02:39:27.863238','2025-12-15 02:39:27.864016'),(152,'test 구글 49','https://google.com','2025-12-15 02:39:27.863246','2025-12-15 02:39:27.864024'),(153,'test 구글 50','https://google.com','2025-12-15 02:39:27.863253','2025-12-15 02:39:27.864031'),(154,'test 구글 51','https://google.com','2025-12-15 02:39:27.863260','2025-12-15 02:39:27.864038'),(155,'test 구글 52','https://google.com','2025-12-15 02:39:27.863268','2025-12-15 02:39:27.864046'),(156,'test 구글 53','https://google.com','2025-12-15 02:39:27.863276','2025-12-15 02:39:27.864053'),(157,'test 구글 54','https://google.com','2025-12-15 02:39:27.863284','2025-12-15 02:39:27.864061'),(158,'test 구글 55','https://google.com','2025-12-15 02:39:27.863291','2025-12-15 02:39:27.864068'),(159,'test 구글 56','https://google.com','2025-12-15 02:39:27.863299','2025-12-15 02:39:27.864076'),(160,'test 구글 57','https://google.com','2025-12-15 02:39:27.863307','2025-12-15 02:39:27.864083'),(161,'test 구글 58','https://google.com','2025-12-15 02:39:27.863314','2025-12-15 02:39:27.864091'),(162,'test 구글 59','https://google.com','2025-12-15 02:39:27.863322','2025-12-15 02:39:27.864098'),(163,'test 구글 60','https://google.com','2025-12-15 02:39:27.863329','2025-12-15 02:39:27.864106'),(164,'test 구글 61','https://google.com','2025-12-15 02:39:27.863337','2025-12-15 02:39:27.864113'),(165,'test 구글 62','https://google.com','2025-12-15 02:39:27.863344','2025-12-15 02:39:27.864121'),(166,'test 구글 63','https://google.com','2025-12-15 02:39:27.863352','2025-12-15 02:39:27.864128'),(167,'test 구글 64','https://google.com','2025-12-15 02:39:27.863359','2025-12-15 02:39:27.864135'),(168,'test 구글 65','https://google.com','2025-12-15 02:39:27.863367','2025-12-15 02:39:27.864143'),(169,'test 구글 66','https://google.com','2025-12-15 02:39:27.863375','2025-12-15 02:39:27.864151'),(170,'test 구글 67','https://google.com','2025-12-15 02:39:27.863382','2025-12-15 02:39:27.864158'),(171,'test 구글 68','https://google.com','2025-12-15 02:39:27.863389','2025-12-15 02:39:27.864166'),(172,'test 구글 69','https://google.com','2025-12-15 02:39:27.863397','2025-12-15 02:39:27.864173'),(173,'test 구글 70','https://google.com','2025-12-15 02:39:27.863404','2025-12-15 02:39:27.864180'),(174,'test 구글 71','https://google.com','2025-12-15 02:39:27.863412','2025-12-15 02:39:27.864188'),(175,'test 구글 72','https://google.com','2025-12-15 02:39:27.863419','2025-12-15 02:39:27.864195'),(176,'test 구글 73','https://google.com','2025-12-15 02:39:27.863426','2025-12-15 02:39:27.864203'),(177,'test 구글 74','https://google.com','2025-12-15 02:39:27.863434','2025-12-15 02:39:27.864210'),(178,'test 구글 75','https://google.com','2025-12-15 02:39:27.863441','2025-12-15 02:39:27.864217'),(179,'test 구글 76','https://google.com','2025-12-15 02:39:27.863448','2025-12-15 02:39:27.864224'),(180,'test 구글 77','https://google.com','2025-12-15 02:39:27.863456','2025-12-15 02:39:27.864232'),(181,'test 구글 78','https://google.com','2025-12-15 02:39:27.863464','2025-12-15 02:39:27.864240'),(182,'test 구글 79','https://google.com','2025-12-15 02:39:27.863471','2025-12-15 02:39:27.864248'),(183,'test 구글 80','https://google.com','2025-12-15 02:39:27.863478','2025-12-15 02:39:27.864255'),(184,'test 구글 81','https://google.com','2025-12-15 02:39:27.863486','2025-12-15 02:39:27.864263'),(185,'test 구글 82','https://google.com','2025-12-15 02:39:27.863493','2025-12-15 02:39:27.864270'),(186,'test 구글 83','https://google.com','2025-12-15 02:39:27.863501','2025-12-15 02:39:27.864278'),(187,'test 구글 84','https://google.com','2025-12-15 02:39:27.863508','2025-12-15 02:39:27.864285'),(188,'test 구글 85','https://google.com','2025-12-15 02:39:27.863516','2025-12-15 02:39:27.864293'),(189,'test 구글 86','https://google.com','2025-12-15 02:39:27.863523','2025-12-15 02:39:27.864300'),(190,'test 구글 87','https://google.com','2025-12-15 02:39:27.863530','2025-12-15 02:39:27.864307'),(191,'test 구글 88','https://google.com','2025-12-15 02:39:27.863538','2025-12-15 02:39:27.864315'),(192,'test 구글 89','https://google.com','2025-12-15 02:39:27.863545','2025-12-15 02:39:27.864322'),(193,'test 구글 90','https://google.com','2025-12-15 02:39:27.863553','2025-12-15 02:39:27.864329'),(194,'test 구글 91','https://google.com','2025-12-15 02:39:27.863560','2025-12-15 02:39:27.864337'),(195,'test 구글 92','https://google.com','2025-12-15 02:39:27.863568','2025-12-15 02:39:27.864344'),(196,'test 구글 93','https://google.com','2025-12-15 02:39:27.863576','2025-12-15 02:39:27.864352'),(197,'test 구글 94','https://google.com','2025-12-15 02:39:27.863583','2025-12-15 02:39:27.864359'),(198,'test 구글 95','https://google.com','2025-12-15 02:39:27.863590','2025-12-15 02:39:27.864366'),(199,'test 구글 96','https://google.com','2025-12-15 02:39:27.863598','2025-12-15 02:39:27.864374'),(200,'test 구글 97','https://google.com','2025-12-15 02:39:27.863605','2025-12-15 02:39:27.864381'),(201,'test 구글 98','https://google.com','2025-12-15 02:39:27.863613','2025-12-15 02:39:27.864388'),(202,'test 구글 99','https://google.com','2025-12-15 02:39:27.863621','2025-12-15 02:39:27.864396');
/*!40000 ALTER TABLE `bookmark_bookmark` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-12-13 15:19:07.656635','1','Bookmark object (1)',1,'[{\"added\": {}}]',7,1),(2,'2025-12-13 15:19:22.407215','1','Bookmark object (1)',2,'[]',7,1),(3,'2025-12-13 15:19:48.511926','2','Bookmark object (2)',1,'[{\"added\": {}}]',7,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'auth','user'),(7,'bookmark','bookmark'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-12-13 14:26:36.560988'),(2,'auth','0001_initial','2025-12-13 14:26:37.175640'),(3,'admin','0001_initial','2025-12-13 14:26:37.334683'),(4,'admin','0002_logentry_remove_auto_add','2025-12-13 14:26:37.342265'),(5,'admin','0003_logentry_add_action_flag_choices','2025-12-13 14:26:37.351244'),(6,'contenttypes','0002_remove_content_type_name','2025-12-13 14:26:37.476674'),(7,'auth','0002_alter_permission_name_max_length','2025-12-13 14:26:37.540030'),(8,'auth','0003_alter_user_email_max_length','2025-12-13 14:26:37.562691'),(9,'auth','0004_alter_user_username_opts','2025-12-13 14:26:37.569990'),(10,'auth','0005_alter_user_last_login_null','2025-12-13 14:26:37.636751'),(11,'auth','0006_require_contenttypes_0002','2025-12-13 14:26:37.640464'),(12,'auth','0007_alter_validators_add_error_messages','2025-12-13 14:26:37.648416'),(13,'auth','0008_alter_user_username_max_length','2025-12-13 14:26:37.717437'),(14,'auth','0009_alter_user_last_name_max_length','2025-12-13 14:26:37.790044'),(15,'auth','0010_alter_group_name_max_length','2025-12-13 14:26:37.809748'),(16,'auth','0011_update_proxy_permissions','2025-12-13 14:26:37.818379'),(17,'auth','0012_alter_user_first_name_max_length','2025-12-13 14:26:37.893267'),(18,'sessions','0001_initial','2025-12-13 14:26:37.931601'),(19,'bookmark','0001_initial','2025-12-13 15:12:30.683784');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('hfcfpoh5a9xgg2i2onlww11urouxbvwb','.eJxVjDsOwjAQBe_iGln-xVlT0nMGa71rcADZUpxUiLuTSCmgnZn33iLiupS49jzHicVZaHH6ZQnpmesu-IH13iS1usxTknsiD9vltXF-XY7276BgL9s6DAQjewwZNAANow_KKQo2QCJnLIBOhg0SbFgnzg4skvU3TwSISny-xOg3fg:1vUSYu:DndSjvC0zHOgEmNhNIbdYp8GbJfXaZosv1mVU8X8kyY','2025-12-27 16:33:40.718035'),('nw5cpr2u7zs3qi4y405d502tla4lb62b','.eJxVjDsOwjAQBe_iGln-xVlT0nMGa71rcADZUpxUiLuTSCmgnZn33iLiupS49jzHicVZaHH6ZQnpmesu-IH13iS1usxTknsiD9vltXF-XY7276BgL9s6DAQjewwZNAANow_KKQo2QCJnLIBOhg0SbFgnzg4skvU3TwSISny-xOg3fg:1vUy1d:Y4lFEySmIeJOthNrHTSsXLZLLD7LOGcYTFGzfapx89o','2025-12-29 02:09:25.409578'),('s7z6t7680cdtdkc4zrlf420sg5hbaas7','.eJxVjDsOwjAQBe_iGln-xVlT0nMGa71rcADZUpxUiLuTSCmgnZn33iLiupS49jzHicVZaHH6ZQnpmesu-IH13iS1usxTknsiD9vltXF-XY7276BgL9s6DAQjewwZNAANow_KKQo2QCJnLIBOhg0SbFgnzg4skvU3TwSISny-xOg3fg:1vUR9q:os-f4xuRkQlLyOwgLnLmgbXx43arpyA9Bn1uuyj8HVY','2025-12-27 15:03:42.000883');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-15 12:16:33
