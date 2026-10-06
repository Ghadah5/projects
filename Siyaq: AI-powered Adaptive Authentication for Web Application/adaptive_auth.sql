-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: adaptive_auth
-- ------------------------------------------------------
-- Server version	9.6.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

-- SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '92769ef5-0b6f-11f1-a2eb-00ffc115eca1:1-76';

--
-- Table structure for table `audit_log`
--

DROP TABLE IF EXISTS `audit_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_log` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `attempt_id` int NOT NULL,
  `user_id` int NOT NULL,
  `event_time` datetime NOT NULL,
  `last_update` datetime DEFAULT NULL,
  `severity_level` enum('Low','Medium','High') NOT NULL,
  PRIMARY KEY (`log_id`),
  KEY `user_id` (`user_id`),
  KEY `audit_log_ibfk_new` (`attempt_id`),
  CONSTRAINT `audit_log_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `audit_log_ibfk_new` FOREIGN KEY (`attempt_id`) REFERENCES `context_snapshot` (`attempt_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_decision`
--

DROP TABLE IF EXISTS `auth_decision`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_decision` (
  `decision_id` int NOT NULL AUTO_INCREMENT,
  `attempt_id` int NOT NULL,
  `action` enum('Standard','MFA','TempLock','AdminLock') NOT NULL,
  `decision_time` datetime NOT NULL,
  PRIMARY KEY (`decision_id`),
  KEY `auth_decision_ibfk_new` (`attempt_id`),
  CONSTRAINT `auth_decision_ibfk_new` FOREIGN KEY (`attempt_id`) REFERENCES `context_snapshot` (`attempt_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `context_snapshot`
--

DROP TABLE IF EXISTS `context_snapshot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `context_snapshot` (
  `attempt_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `attempt_time` datetime NOT NULL,
  `success` tinyint(1) NOT NULL,
  `failed_attempts_count` int DEFAULT '0',
  `ip_address` varchar(45) NOT NULL,
  `geo_country` varchar(50) DEFAULT NULL,
  `geo_city` varchar(50) DEFAULT NULL,
  `os` varchar(50) DEFAULT NULL,
  `browser` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`attempt_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `fk_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;

CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `first_name` char(50) NOT NULL,
  `last_name` char(50) NOT NULL,
  `national_id` varchar(20) NOT NULL,
  `email` char(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` char(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `user_role` enum('Normal user','Admin') NOT NULL DEFAULT 'Normal user',
  `status` enum('Active','TempLocked','AdminLocked') NOT NULL DEFAULT 'Active',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-11  3:06:30

ALTER TABLE user 
ADD COLUMN is_verified TINYINT(1) NOT NULL DEFAULT 0;

CREATE TABLE email_verification (
    verification_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    verification_code VARCHAR(10) NOT NULL,
    expires_at DATETIME NOT NULL,
    used TINYINT(1) DEFAULT 0,

    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
