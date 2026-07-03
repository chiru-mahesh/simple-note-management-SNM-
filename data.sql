-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: snm29db
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `filedata`
--

DROP TABLE IF EXISTS `filedata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `filedata` (
  `fileid` int unsigned NOT NULL AUTO_INCREMENT,
  `filename` longtext,
  `filedata` longblob,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `userid` int unsigned DEFAULT NULL,
  PRIMARY KEY (`fileid`),
  KEY `userid` (`userid`),
  CONSTRAINT `filedata_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `userdata` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filedata`
--

LOCK TABLES `filedata` WRITE;
/*!40000 ALTER TABLE `filedata` DISABLE KEYS */;
INSERT INTO `filedata` VALUES (1,'multidict.py',_binary '\'\'\'employee= {}\r\n\r\nwhile True:\r\n    print(\"\\n Employee Management System\")\r\n    print(\"1. Add Employee\")\r\n    print(\"2. Access Employee Details\")\r\n    print(\"3. Update Employee Details\")\r\n    print(\"4. Delete Employee\")\r\n    print(\"5. Display All Employees\")\r\n    print(\"6. Exit\")\r\n\r\n    choice = input(\"Enter your choice: \")\r\n\r\n    if choice == \"1\":\r\n        emp_id = input(\"Enter Employee ID: \")\r\n        name = input(\"Enter Name: \")\r\n        age = int(input(\"Enter Age: \"))\r\n        department = input(\"Enter Department: \")\r\n\r\n        employees[emp_id] = {\r\n            \"Name\": name,\r\n            \"Age\": age,\r\n            \"Department\": department\r\n        }\r\n\r\n        print(\"Employee added successfully!\")\r\n\r\n    elif choice == \"2\":\r\n        emp_id = input(\"Enter Employee ID to access: \")\r\n\r\n        if emp_id in employees:\r\n            print(\"Employee Details:\")\r\n            print(employees[emp_id])\r\n        else:\r\n            print(\"Employee not found!\")\r\n\r\n    elif choice == \"3\":\r\n        emp_id = input(\"Enter Employee ID to update: \")\r\n\r\n        if emp_id in employees:\r\n            name = input(\"Enter New Name: \")\r\n            age = int(input(\"Enter New Age: \"))\r\n            department = input(\"Enter New Department: \")\r\n\r\n            employees[emp_id][\"Name\"] = name\r\n            employees[emp_id][\"Age\"] = age\r\n            employees[emp_id][\"Department\"] = department\r\n\r\n            print(\"Employee details updated successfully!\")\r\n        else:\r\n            print(\"Employee not found!\")\r\n\r\n    elif choice == \"4\":\r\n        emp_id = input(\"Enter Employee ID to delete: \")\r\n\r\n        if emp_id in employees:\r\n            del employees[emp_id]\r\n            print(\"Employee deleted successfully!\")\r\n        else:\r\n            print(\"Employee not found!\")\r\n\r\n    elif choice == \"5\":\r\n        if employees:\r\n            print(\"\\nAll Employee Details:\")\r\n            for emp_id, details in employees.items():\r\n                print(f\"\\nEmployee ID: {emp_id}\")\r\n                for key, value in details.items():\r\n                    print(f\"{key}: {value}\")\r\n        else:\r\n            print(\"No employees available!\")\r\n\r\n    elif choice == \"6\":\r\n        print(\"Exiting Program...\")\r\n        break\r\n\r\n    else:\r\n        print(\"Invalid choice! Please try again.\")\r\n\r\n \'\'\'       \r\n\r\n\r\nemployees = {}\r\n\r\n\r\nid = input(\"Enter Employee ID: \")\r\nname = input(\"Enter Name: \")\r\nemployees[id] = name\r\n\r\n\r\nprint(\"Employee Details:\", employees[id])\r\n\r\n\r\nnew_name = input(\"Enter New Name: \")\r\nemployees[id] = new_name\r\nprint(\"Updated Details:\", employees[id])\r\n\r\n\r\ndel employees[id]\r\nprint(\"Employee Deleted\")\r\n\r\n\r\nprint(\"Employees:\", employees)\r\n','2026-06-30 19:50:59',1),(4,'hashing.py','','2026-06-30 19:55:41',1);
/*!40000 ALTER TABLE `filedata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notesdata`
--

DROP TABLE IF EXISTS `notesdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notesdata` (
  `notesid` int unsigned NOT NULL AUTO_INCREMENT,
  `title` longtext,
  `description` longtext,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `userid` int unsigned DEFAULT NULL,
  PRIMARY KEY (`notesid`),
  KEY `userid` (`userid`),
  CONSTRAINT `notesdata_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `userdata` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notesdata`
--

LOCK TABLES `notesdata` WRITE;
/*!40000 ALTER TABLE `notesdata` DISABLE KEYS */;
INSERT INTO `notesdata` VALUES (4,'flask',' it is a micro web framework for Python language..','2026-06-27 15:18:29',1),(5,'cyber security','ethical hacking','2026-06-27 15:18:59',1),(6,'python','programming language','2026-06-30 13:44:23',1);
/*!40000 ALTER TABLE `notesdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userdata`
--

DROP TABLE IF EXISTS `userdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userdata` (
  `userid` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `useremail` varchar(50) NOT NULL,
  `password` varchar(40) DEFAULT NULL,
  `phone_num` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`userid`),
  UNIQUE KEY `useremail` (`useremail`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userdata`
--

LOCK TABLES `userdata` WRITE;
/*!40000 ALTER TABLE `userdata` DISABLE KEYS */;
INSERT INTO `userdata` VALUES (1,'mahesh','mahesh520004@gmail.com','Chiru mahesh@23','9963019761');
/*!40000 ALTER TABLE `userdata` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-03 14:20:34
