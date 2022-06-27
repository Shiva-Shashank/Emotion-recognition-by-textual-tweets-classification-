-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.0.22-community-nt


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


--
-- Create schema happy
--

CREATE DATABASE IF NOT EXISTS happy;
USE happy;

--
-- Definition of table `main`
--

DROP TABLE IF EXISTS `main`;
CREATE TABLE `main` (
  `Id` int(10) unsigned NOT NULL auto_increment,
  `news_content` varchar(1000) NOT NULL,
  `pred` varchar(100) NOT NULL,
  `userid` varchar(45) NOT NULL,
  PRIMARY KEY  (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `main`
--

/*!40000 ALTER TABLE `main` DISABLE KEYS */;
INSERT INTO `main` (`Id`,`news_content`,`pred`,`userid`) VALUES 
 (1,'@LodurZJ Well pizza... but that is good too! ','Happy','2'),
 (3,'HOLD THIS PHAT L DEPRESSION  https://twitter.com/pvlkvsky/status/989183405240868865Ã‚Â Ã¢Â€Â¦','Unhappy','1');
/*!40000 ALTER TABLE `main` ENABLE KEYS */;


--
-- Definition of table `register`
--

DROP TABLE IF EXISTS `register`;
CREATE TABLE `register` (
  `Id` int(10) unsigned NOT NULL auto_increment,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY  (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `register`
--

/*!40000 ALTER TABLE `register` DISABLE KEYS */;
INSERT INTO `register` (`Id`,`username`,`email`,`password`) VALUES 
 (1,'vidhya','santhoshrobotai@gmail.com','Sandy@123'),
 (2,'santhosh','santhosh@gmail.com','Sandy@123'),
 (3,'sathish','sonsandy1993@gmail.com','Sandy@123');
/*!40000 ALTER TABLE `register` ENABLE KEYS */;




/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
