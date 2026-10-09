CREATE DATABASE  IF NOT EXISTS `hospital` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `hospital`;
-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: hospital
-- ------------------------------------------------------
-- Server version	8.0.30

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

--
-- Table structure for table `manages`
--

DROP TABLE IF EXISTS `manages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manages` (
  `medicalID` int NOT NULL,
  `MedicineID` int NOT NULL,
  PRIMARY KEY (`medicalID`,`MedicineID`),
  KEY `Manages_FK2` (`MedicineID`),
  CONSTRAINT `Manages_FK1` FOREIGN KEY (`medicalID`) REFERENCES `medicalstaff` (`idNumber`),
  CONSTRAINT `Manages_FK2` FOREIGN KEY (`MedicineID`) REFERENCES `medicine` (`idNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manages`
--

LOCK TABLES `manages` WRITE;
/*!40000 ALTER TABLE `manages` DISABLE KEYS */;
INSERT INTO `manages` VALUES (1120917163,507465),(1005695598,1276500),(1120917163,3330544),(1120917163,4320067),(1005695598,5566321);
/*!40000 ALTER TABLE `manages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicalstaff`
--

DROP TABLE IF EXISTS `medicalstaff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicalstaff` (
  `idNumber` int NOT NULL,
  `fName` varchar(10) DEFAULT NULL,
  `minit` varchar(10) DEFAULT NULL,
  `lName` varchar(10) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `specialization` varchar(20) DEFAULT NULL,
  `super_id` int DEFAULT NULL,
  PRIMARY KEY (`idNumber`),
  UNIQUE KEY `idNumber` (`idNumber`),
  KEY `MedicalStaff_FK1` (`super_id`),
  CONSTRAINT `MedicalStaff_FK1` FOREIGN KEY (`super_id`) REFERENCES `medicalstaff` (`idNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicalstaff`
--

LOCK TABLES `medicalstaff` WRITE;
/*!40000 ALTER TABLE `medicalstaff` DISABLE KEYS */;
INSERT INTO `medicalstaff` VALUES (1005695222,'Asmaa','Walid','Alats','female','pediatrician',1120917163),(1005695598,'Mohammed','Yahia','Albishri','male','internaldoctor',1120917163),(1007180207,'Ahmad','Massad','Alharthi','male','generalSurgeon',1120917163),(1120344163,'Anas','Jamal','Saggaf','male','surgrydoctor',1120917163),(1120917163,'Assayil','Asaad','Hawsawi','female','dentalconsultant',NULL);
/*!40000 ALTER TABLE `medicalstaff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicine`
--

DROP TABLE IF EXISTS `medicine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicine` (
  `idNumber` int NOT NULL,
  `medicineName` varchar(20) DEFAULT NULL,
  `price` int DEFAULT NULL,
  PRIMARY KEY (`idNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicine`
--

LOCK TABLES `medicine` WRITE;
/*!40000 ALTER TABLE `medicine` DISABLE KEYS */;
INSERT INTO `medicine` VALUES (507465,'Buscopan',60),(1276500,'Cidamex',200),(3330544,'Adolsinus',50),(4320067,'After-meals',118),(5566321,'Bepra',158);
/*!40000 ALTER TABLE `medicine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `idNumber` int DEFAULT NULL,
  `fName` varchar(10) DEFAULT NULL,
  `minit` varchar(10) DEFAULT NULL,
  `lName` varchar(20) DEFAULT NULL,
  `birthDate` date DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `fileNumber` int NOT NULL,
  PRIMARY KEY (`fileNumber`),
  UNIQUE KEY `idNumber` (`idNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (1115695598,'Zahraa','Ali','Alshahri','1985-03-07','female',100364),(1007180277,'ibrahem','Abdullah','Alzahrani','1991-12-05','male',112300),(1005698872,'Ghozlan','Akram','Busha','2000-11-08','female',112367),(1120990361,'Najwan','Suleiman','Orif','2004-03-04','female',115399),(1120919876,'Sami','Asaad','Saggaf','1995-05-23','male',120100);
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patientloc`
--

DROP TABLE IF EXISTS `patientloc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patientloc` (
  `pFileNumber` int NOT NULL,
  `location` varchar(40) NOT NULL,
  PRIMARY KEY (`pFileNumber`,`location`),
  CONSTRAINT `PatientLoc_FK1` FOREIGN KEY (`pFileNumber`) REFERENCES `patient` (`fileNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patientloc`
--

LOCK TABLES `patientloc` WRITE;
/*!40000 ALTER TABLE `patientloc` DISABLE KEYS */;
INSERT INTO `patientloc` VALUES (100364,'Altanaim '),(112300,'Alawali '),(112300,'Alaziziyah '),(112367,'Alrashidiya '),(115399,'Alshawqiyya'),(120100,'Alzahir ');
/*!40000 ALTER TABLE `patientloc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patientphone`
--

DROP TABLE IF EXISTS `patientphone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patientphone` (
  `pFileNumber` int NOT NULL,
  `phoneNumber` int NOT NULL,
  PRIMARY KEY (`pFileNumber`,`phoneNumber`),
  CONSTRAINT `PatientPhone_FK1` FOREIGN KEY (`pFileNumber`) REFERENCES `patient` (`fileNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patientphone`
--

LOCK TABLES `patientphone` WRITE;
/*!40000 ALTER TABLE `patientphone` DISABLE KEYS */;
INSERT INTO `patientphone` VALUES (100364,555054263),(100364,558991226),(112300,552888163),(112367,566972247),(115399,507343755);
/*!40000 ALTER TABLE `patientphone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reception`
--

DROP TABLE IF EXISTS `reception`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reception` (
  `employeeId` int NOT NULL,
  `fName` varchar(10) DEFAULT NULL,
  `minit` varchar(10) DEFAULT NULL,
  `lName` varchar(20) DEFAULT NULL,
  `gender` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`employeeId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reception`
--

LOCK TABLES `reception` WRITE;
/*!40000 ALTER TABLE `reception` DISABLE KEYS */;
INSERT INTO `reception` VALUES (1067760207,'Reem','Mohammed','Alharbi','female'),(1143656457,'Amal','Yousef','Alharthi','female'),(1144859027,'Lama','Abdulaziz','Alotaibi','female'),(1159875650,'Batal','Omar','Alqahtani','male'),(1197180203,'Ali','Saud','Theban','male');
/*!40000 ALTER TABLE `reception` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `takes`
--

DROP TABLE IF EXISTS `takes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `takes` (
  `pFileNumber` int NOT NULL,
  `MedicineID` int NOT NULL,
  PRIMARY KEY (`pFileNumber`,`MedicineID`),
  KEY `Takes_FK2` (`MedicineID`),
  CONSTRAINT `Takes_FK1` FOREIGN KEY (`pFileNumber`) REFERENCES `patient` (`fileNumber`),
  CONSTRAINT `Takes_FK2` FOREIGN KEY (`MedicineID`) REFERENCES `medicine` (`idNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `takes`
--

LOCK TABLES `takes` WRITE;
/*!40000 ALTER TABLE `takes` DISABLE KEYS */;
INSERT INTO `takes` VALUES (100364,507465),(112367,1276500),(112300,3330544),(112367,4320067),(115399,5566321);
/*!40000 ALTER TABLE `takes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visit`
--

DROP TABLE IF EXISTS `visit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `visit` (
  `pFileNumber` int NOT NULL,
  `employeeId` int NOT NULL,
  `medicalID` int NOT NULL,
  `price` int DEFAULT NULL,
  PRIMARY KEY (`pFileNumber`,`employeeId`,`medicalID`),
  KEY `Visit_FK2` (`medicalID`),
  KEY `Visit_FK3` (`employeeId`),
  CONSTRAINT `Visit_FK1` FOREIGN KEY (`pFileNumber`) REFERENCES `patient` (`fileNumber`),
  CONSTRAINT `Visit_FK2` FOREIGN KEY (`medicalID`) REFERENCES `medicalstaff` (`idNumber`),
  CONSTRAINT `Visit_FK3` FOREIGN KEY (`employeeId`) REFERENCES `reception` (`employeeId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visit`
--

LOCK TABLES `visit` WRITE;
/*!40000 ALTER TABLE `visit` DISABLE KEYS */;
INSERT INTO `visit` VALUES (100364,1159875650,1005695598,300),(112300,1197180203,1007180207,500),(112367,1143656457,1005695598,750),(115399,1067760207,1120917163,200);
/*!40000 ALTER TABLE `visit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visitor`
--

DROP TABLE IF EXISTS `visitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `visitor` (
  `pFileNumber` int NOT NULL,
  `fName` varchar(10) NOT NULL,
  `lName` varchar(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `relationsship` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`pFileNumber`,`fName`),
  CONSTRAINT `Visitor_FK1` FOREIGN KEY (`pFileNumber`) REFERENCES `patient` (`fileNumber`),
  CONSTRAINT `visitor_chk_1` CHECK ((`age` > 18))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visitor`
--

LOCK TABLES `visitor` WRITE;
/*!40000 ALTER TABLE `visitor` DISABLE KEYS */;
INSERT INTO `visitor` VALUES (100364,'Rawan','Alharbi','female',44,'Mother'),(112300,'Maryam','Alharbi','female',25,'Wife'),(112367,'Samara','Busha','female',23,'Sister'),(115399,'Suleiman','Orif','male',47,'Fhather'),(120100,'Saad','Saggaf','male',28,'Brother');
/*!40000 ALTER TABLE `visitor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-02  6:50:28
