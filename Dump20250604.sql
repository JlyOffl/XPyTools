-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 192.168.0.179    Database: TwitterExplorer
-- ------------------------------------------------------
-- Server version	5.5.5-10.11.6-MariaDB-0+deb12u1

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
-- Table structure for table `Following`
--

DROP TABLE IF EXISTS `Following`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Following` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `UserName` varchar(100) NOT NULL,
  `DisplayName` varchar(200) DEFAULT NULL,
  `bAutoRecord` tinyint(1) DEFAULT NULL,
  `SpeakerCount` int(11) DEFAULT 0,
  `HostCount` int(11) DEFAULT 0,
  `LastActivity` datetime NULL,
  `MainUser` int(11) DEFAULT 0,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `idx_username` (`UserName`)
) ENGINE=InnoDB AUTO_INCREMENT=28381321 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Following`
--

LOCK TABLES `Following` WRITE;
/*!40000 ALTER TABLE `Following` DISABLE KEYS */;
INSERT INTO `Following` VALUES (4,'Maransadagopan','Magizhmaran ❇️',0,0,0,'2024-06-11 13:25:27',1),(11,'mindgage','Sheriff Ali Ibn El Kharish',1,0,0,'2024-06-11 13:25:27',1),(14,'nolan_moor','Adam நோலன்',0,0,0,'2024-06-11 13:25:27',1),(22,'Karthikravivarm','Karthik Ravivarma',1,0,0,'2024-06-11 13:25:27',1),(24,'htilah21','Haalith',NULL,0,0,'2024-06-11 13:25:27',1),(25,'aarathniya','❤️‍? ? அதிதி ❤️‍??',NULL,0,0,'2024-06-11 13:25:27',1),(27,'karikalaseelan','கரிகால சீலன்',0,0,0,'2024-06-11 13:25:27',1),(34,'Shivasakthi238','கமலி❤️',NULL,0,0,'2024-06-11 13:25:27',1),(36,'dhushy63','Chitti',0,0,0,'2024-06-11 13:25:27',1),(49,'senthil09562484','சுமீ.செந்தில்குமார்',NULL,0,0,'2024-06-11 13:25:27',1),(10907,'bala4379959146','Bala',0,0,0,'2024-06-12 07:12:05',1),(26389,'gracianvaddaka','ஐயாச்சி',0,0,0,'2024-06-12 15:31:05',1),(102136,'DrGanesh_Japan','முனைவர். கணேசு ガネス',NULL,0,0,'2024-06-14 09:34:25',1),(110155,'AIIMS_COVAI','வடகலை ஜடிலன் ஐயங்கார்',0,0,0,'2024-06-14 14:23:10',1),(147678,'nimalan2601','Nimalan',0,0,0,'2024-06-15 11:07:17',1),(211892,'kartiloki','?︎?︎?︎?︎ ?︎?︎?︎?︎?︎',0,0,0,'2024-06-17 00:09:47',1),(275708,'ChiyanSaamy','சாமி ?⚡',0,0,0,'2024-06-18 11:41:30',1),(318386,'nallalavaruman','நல்லாளவருமன்',0,0,0,'2024-06-19 10:57:35',1),(322554,'SurendarRPG','TimeoutError',0,0,0,'2024-06-19 13:29:02',1),(338691,'pidisambal','பிடிசாம்பல்',0,0,0,'2024-06-19 22:48:22',1),(384795,'smurugesanadmk','முருகேசன் சுப்ரமணி (M.B.A.,)',0,0,0,'2024-06-21 01:46:44',1),(402360,'ThiranAayvidam','திறன் ஆய்விடம்',0,0,0,'2024-06-21 12:10:59',1),(438008,'mandalorian96','Lite yagami',NULL,0,0,'2024-06-22 09:41:16',1),(1441561,'samuraijackk99','Mithun ஆசீவகன்',NULL,0,0,'2024-07-07 05:01:16',1),(2606107,'Dr_Anil_2','TimeoutError',1,0,0,'2024-07-23 11:46:15',1),(2642732,'DHEERAN1077','?புலிக்குட்டி✨',NULL,0,0,'2024-07-23 23:54:06',1),(2643018,'reese2550','Morattu kaalayan',NULL,0,0,'2024-07-23 23:58:55',1),(2676554,'tweettopals','Dr.Pals',NULL,0,0,'2024-07-24 11:08:10',1),(3032127,'priyan23222','priyan ? (இளஞ்செழியன்)',NULL,0,0,'2024-07-29 10:46:54',1),(3180334,'PrakashMahadev','Prakash Mahadevan',NULL,0,0,'2024-07-31 11:59:05',1),(3335252,'magizhmaaran','அசால்ட்டு சேது',1,0,0,'2024-08-02 17:44:01',1),(3528777,'The_69_Percent','காளி',0,0,0,'2024-08-05 10:23:57',1),(6334789,'samiraj_04','சாமிராஜ்',NULL,0,0,'2024-09-13 12:50:38',1),(6518812,'Sheik_207','?Sheik☀',NULL,0,0,'2024-09-16 12:39:58',1),(7285391,'PRspacess','PR',1,0,0,'2024-09-27 03:57:06',1),(7381002,'mrpaluvets','Mr.பழுவேட்டரையர்',1,0,0,'2024-09-28 11:49:48',1),(7387311,'thamizh975111','தமிழ்அரசன்',1,0,0,'2024-09-28 13:58:34',1),(8102540,'DevakiR','Maha Deva',0,0,0,'2024-10-08 15:13:46',1),(8105374,'kajan1215','கரன்',NULL,0,0,'2024-10-08 16:11:11',1),(8143681,'LeagueRed58401','RedLeague',0,1,0,'2024-10-09 05:03:27',1),(8160583,'TNCCITSMSpaces','TNCC IT & SM Dept Spaces',1,0,0,'2024-10-09 10:43:31',1),(8367680,'Harish_NS149','Harish N S',NULL,0,0,'2024-10-12 08:30:15',1),(9075075,'RameshR66484129','?தமிழன்? சூரமலையான்??',1,0,0,'2024-10-22 08:52:55',1),(9440794,'seelanano','இராவணன்',1,0,0,'2024-10-27 12:20:31',1),(9585455,'tamilcinema_12','????? ?????? ?????',NULL,0,0,'2024-10-29 13:12:40',1),(10410822,'TravidaThamizha','திராவிட தமிழன்',NULL,0,0,'2024-11-10 05:20:07',1),(10643833,'sudhakar4258','சுதாகர் பாரத நாடு',NULL,0,0,'2024-11-13 11:57:21',1),(11352972,'AskAatukutti','Madam’sAdam-Yakuza-Mamakuttyyyy ?',NULL,0,0,'2024-11-23 13:27:28',1),(11406029,'razorturbokat','Razor',NULL,0,0,'2024-11-24 07:19:23',1),(12484432,'walloftamizh','Dr.Dom Terroto',0,0,0,'2024-12-09 12:26:43',1),(12684931,'Orange_Mittaai','ஆர்த்தி பார்கவன் ❤',NULL,0,0,'2024-12-12 08:36:09',1),(12903085,'rkrish14692','KrishnanMurali',NULL,1,0,'2024-12-15 10:43:55',1),(13111592,'Chandrumlpt','ABD',1,0,0,'2024-12-18 10:32:54',1),(13271138,'Thakkar2024','தக்கார்',NULL,0,0,'2024-12-20 17:09:51',1),(13755328,'Velmuru51716413','Velmurugan',NULL,0,0,'2024-12-27 09:32:02',1),(14674494,'megna312','Meghna',NULL,0,0,'2025-01-05 10:21:12',1),(14680514,'YEM_AAR','பேரலை',NULL,0,0,'2025-01-05 11:43:17',1),(14707441,'FunGunRunMun','அ兀❤️?ᴹᵃⁿⁱராஜ்₿',NULL,0,0,'2025-01-05 18:15:09',1),(14769425,'Pudhiyavanoffl','Pudhiyavan (புதியவன்)',1,0,0,'2025-01-06 09:37:04',1),(14791199,'stringsradio','SoundBox',NULL,0,0,'2025-01-06 14:37:21',1),(15786063,'me_lilipoo','ℓιℓℓιвєт ??',NULL,0,0,'2025-01-16 06:07:18',1),(15791955,'Ondragaofficial','Ondraga',1,0,0,'2025-01-16 07:29:13',1),(15808593,'jjilladi007','சேவலதிகாரம்',1,0,0,'2025-01-16 11:05:38',1),(16012458,'araikuraikavi88','RJ பாலன் சிவா',NULL,0,0,'2025-01-18 10:41:23',1),(16107156,'TenkasiSubraman','தென்காசி சுப்பிரமணியன் Tenkasi Subramanian',NULL,0,0,'2025-01-19 10:35:21',1),(16110146,'off_rrajesh','?இராஜேஷ்?',NULL,0,0,'2025-01-19 11:16:41',1),(16184807,'redpuzzle24','Abhishek Mahadevan',NULL,0,0,'2025-01-20 04:53:54',1),(16193720,'charmfulGrace','??',1,0,0,'2025-01-20 06:51:43',1),(16204666,'Ramesh88298556','Wolf pack ( மோடிக்கும் எனக்கும் சம்பந்தம் இல்லை )',1,0,0,'2025-01-20 09:43:21',1),(16210101,'akarchstudio1','ArCHaNa AK',NULL,0,0,'2025-01-20 11:13:53',1),(16370798,'Ranjith_R23','மேதகு Panther',1,0,0,'2025-01-22 03:21:52',1),(17378448,'offkeeran2','TimeoutError',NULL,0,0,'2025-02-01 15:17:07',1),(17411654,'ItzmeSumo','சுமோ',1,0,0,'2025-02-02 00:28:51',1),(17852794,'_gowrisankar_07','Gowrisankar ??',NULL,0,0,'2025-02-06 09:47:28',1),(17880565,'iPraVyn','iPraVyn',NULL,0,0,'2025-02-06 16:23:17',1),(17982469,'sidthedoctor','Sid ?',NULL,0,0,'2025-02-07 18:55:53',1),(18445999,'rrajadvk','Ra.Ra',NULL,0,0,'2025-02-12 09:48:10',1),(18658966,'tamilan_04','Col.Stauffenberg',NULL,0,0,'2025-02-14 11:12:14',1),(18660205,'boomiyenamsami','?பூமியே _நம் _சாமி',NULL,0,0,'2025-02-14 11:31:55',1),(18674745,'Perunchithiran4','பெருஞ்சித்திரனார்',NULL,0,0,'2025-02-14 14:52:25',1),(18759701,'irrungabhai','irrunga bhai memes ??nationalist zone ༗????',NULL,0,0,'2025-02-15 09:31:56',1),(18765034,'superstar_srini','Whistlepodu ??',NULL,0,0,'2025-02-15 10:44:47',1),(18769999,'nadodi_fm','நாடோடி பண்பலை',NULL,0,0,'2025-02-15 11:55:46',1),(20866652,'Shiva25584','Sivasubramaniyam J (MBA.,)',NULL,0,0,'2025-03-08 10:37:22',1),(20925662,'Karnan180','Karnan',NULL,0,0,'2025-03-09 03:13:16',1),(20954026,'bala1422578','?பாலா?',NULL,0,0,'2025-03-09 09:34:12',1),(21070600,'KathisKumaravel','Kathis Kumaravel (மாதொருபாகன் ஜனதா கட்சி விரோதி)',NULL,0,0,'2025-03-10 12:42:11',1),(21317846,'AIADMKITWINGOFL','AIADMK IT WING - SayYesToWomenSafety&AIADMK',NULL,0,0,'2025-03-13 01:49:31',1),(22215516,'pandiyah1','SPN',NULL,0,0,'2025-03-22 07:26:45',1),(22219367,'javaaaa_dev','{ஜாவா}',NULL,0,0,'2025-03-22 08:26:56',1),(22219524,'bioproee','Tamizhpulavan( BM101)',NULL,0,0,'2025-03-22 08:29:12',1),(22251318,'Senthil2025h','வேடன்',NULL,0,0,'2025-03-22 17:15:16',1),(22398716,'Ranjith_Rayappa','Black Panther',1,0,0,'2025-03-24 07:37:41',1),(22518679,'stoppievijay','வி.வி.கே\'s Parody',NULL,0,0,'2025-03-25 12:28:49',1),(22605857,'haraappan','Haraappan',1,0,0,'2025-03-26 10:46:25',1),(22617331,'Tamil_bully','TimeoutError',NULL,0,0,'2025-03-26 13:18:59',1),(22854222,'sureshlal','??Suresh लाल #தருமி??',NULL,0,0,'2025-03-29 04:23:05',1),(22866920,'dragon_R11','வெள்ளமனசு',NULL,0,0,'2025-03-29 07:18:30',1),(23168741,'sivaneshwaran_3','Sivakasi Sivaneshwaran',NULL,0,0,'2025-04-01 11:38:44',1),(23173748,'alamelu_bjp','alamu',NULL,0,0,'2025-04-01 12:51:53',1),(23174674,'salamandra12','Reuben',NULL,0,0,'2025-04-01 13:04:47',1),(23444339,'Ravanachi1','சுவேதா இராவணச்சி',NULL,0,0,'2025-04-04 12:21:57',1),(23557966,'machi199090','மச்சி',NULL,0,0,'2025-04-05 17:07:26',1),(26550227,'ItzKrish_','கிருஷ்ணன்♥️',NULL,0,0,'2025-05-05 13:52:10',1),(26557291,'VeeranRavanan','வீரன்',NULL,0,0,'2025-05-05 15:55:07',1),(26679232,'ImsWarroom3','IMSWARROOM3',NULL,0,0,'2025-05-07 03:41:53',1),(26761762,'BBack87684','Bala Come Back',NULL,0,0,'2025-05-08 03:21:25',1),(26792442,'Nagaraj2303','MGR Naga Raj -(எம்ஜிஆர்.நாகராஜ்)',NULL,0,0,'2025-05-08 12:26:44',1),(26871219,'KKabadii','? மாறா ?',NULL,0,0,'2025-05-09 11:25:35',1),(26875962,'KannappanPaari','சாதீ/குடி (பெருமை) அற்றவன்',NULL,0,0,'2025-05-09 12:43:15',1),(27087588,'itzme_deadshot','Deadshot',NULL,0,0,'2025-05-12 04:39:38',1),(27308315,'gbarani2','Barani',NULL,0,0,'2025-05-15 04:03:53',1),(27333234,'Tobi_hatake_','TENMA (star boy)',NULL,0,0,'2025-05-15 12:31:26',1),(27340204,'Singa_Perumaal','சேது',NULL,0,0,'2025-05-15 14:48:36',1),(27350475,'MrCongenialiti','aako',NULL,0,0,'2025-05-15 18:21:36',1),(27477296,'sumo_sottai1','சொட்ட சுமோ கெட்ட சுமோ',NULL,0,0,'2025-05-17 11:10:58',1),(27684387,'i_chandlerbing','Chandler Bing',NULL,0,0,'2025-05-20 11:50:42',1),(27696167,'RoiEelam','அரசன்',NULL,0,0,'2025-05-20 17:11:49',1),(27722127,'kabali2022','கரடி மூஞ்சி குமாரு',NULL,0,0,'2025-05-21 05:44:03',1),(27760664,'saktheez','???????',NULL,0,0,'2025-05-21 23:00:42',1),(27766207,'emilan2823191','எமிலன் விவசாயி',NULL,0,0,'2025-05-22 02:44:39',1),(27766211,'EURONGREYJOY007','Dr. 2G Spectrum ? ?',NULL,0,0,'2025-05-22 02:45:01',1),(27778759,'Bypavithra03','?Pavithra ??',NULL,0,0,'2025-05-22 10:48:35',1),(27781625,'GopalUrangapuli','தமிழ் வேந்தன்',NULL,0,0,'2025-05-22 12:35:09',1),(27796269,'thennatan2','தென்நாட்டான் சுடுகாட்டு சண்டாளன்',NULL,0,0,'2025-05-22 21:30:45',1),(27803707,'TweetofPKS','Fakendra Modi',NULL,0,0,'2025-05-23 01:56:40',1),(27817674,'MuKa1970','மு.க ?♥️',NULL,0,0,'2025-05-23 10:08:47',1),(27820803,'visu_vasan','Ammai Appar',NULL,0,0,'2025-05-23 11:56:03',1),(27824914,'Ajjju__','αׂׅׅ݂ʝׅ֗✧?',NULL,0,0,'2025-05-23 14:09:25',1),(27828584,'Sundarvap','Sundar Parthasarathy',NULL,0,0,'2025-05-23 16:02:54',1),(27850259,'Tsubramaniyan14','எல்லாம் நன்மைக்கே!',NULL,0,0,'2025-05-24 03:55:25',1),(27890008,'ArunRose_100','தங்கமகன் 100',NULL,0,0,'2025-05-25 01:09:49',1),(27905159,'SJForumindia','Social Justice Forum',NULL,0,0,'2025-05-25 08:58:34',1),(27905846,'ScorpionSu58042','Surendar TVK ?',NULL,0,0,'2025-05-25 09:19:49',1),(27907860,'xAI_Avatar','Avatar',NULL,0,0,'2025-05-25 10:20:36',1),(27935940,'kuthiraioffcial','குதிரை',NULL,0,0,'2025-05-26 00:06:38',1),(27938322,'annanthemass','Mr Adolf ?',NULL,0,0,'2025-05-26 01:16:31',1),(27951822,'kalaiArt11','kalai Art',NULL,0,0,'2025-05-26 07:35:42',1),(27952569,'vanni_1991','Vino⚡️',NULL,0,0,'2025-05-26 07:57:02',1),(27956805,'monstertvk','???????ᵀⱽᴷ?',NULL,0,0,'2025-05-26 09:54:31',1),(27960545,'RatnaKing20','இரத்தினராசா /இரட்ணா',NULL,0,0,'2025-05-26 11:34:54',1),(27962360,'JDALEXtweets','ʲᵈᴀʟᴇxᴀɴᴅᴇʀᵗʷᵉᵉᵗˢ',NULL,0,0,'2025-05-26 12:34:25',1),(27962518,'Akashbcm','Akash santhosh',NULL,0,0,'2025-05-26 12:40:10',1),(27962520,'an82angel','Angel',NULL,0,0,'2025-05-26 12:40:17',1),(27963029,'Moose96013782','Random_tandem',NULL,0,0,'2025-05-26 12:58:39',1),(27963549,'PetersonAnanth','பெருவளத்தான் ?????????????',NULL,0,0,'2025-05-26 13:16:58',1),(27965040,'prasanthking123','Sai Prasanth',NULL,0,0,'2025-05-26 14:11:18',1),(28002982,'yaaro_offl','யாரோ',NULL,0,0,'2025-05-27 12:48:13',1),(28048499,'amlonelywarrior','அறம்பேசுபவன் சோழன்',NULL,0,0,'2025-05-28 14:38:52',1),(28061459,'AasaiThilipan','ஆசைத்தம்பி',NULL,0,0,'2025-05-28 21:33:38',1),(28069612,'Eniyavan_offi26','?ITS ME DHINA✍?',NULL,0,0,'2025-05-29 02:04:25',1),(28072114,'kali15061996','காளி',NULL,0,0,'2025-05-29 03:24:15',1),(28077709,'itskeeran','Keeran',NULL,0,0,'2025-05-29 06:21:54',1),(28085278,'rocket_isro','Rocket(ARTU)?',NULL,0,0,'2025-05-29 10:15:17',1),(28089780,'DrPrabhaOffical','Mr.Comrade ❤️',NULL,0,0,'2025-05-29 12:30:27',1),(28122575,'Sanghi_Hunter_','EMINƎM',NULL,0,0,'2025-05-30 11:04:40',1),(28125918,'media_tbs','TBS Media',NULL,0,0,'2025-05-30 12:39:15',1),(28154037,'shrivathsan79','??קאוויה תלאיבן?? 3.0',NULL,0,0,'2025-05-31 01:48:05',1),(28154778,'Naaikutty_1','இனியவன்',NULL,0,0,'2025-05-31 02:08:34',1),(28168465,'dravidanadu1925','Dravida Udanpirappu',NULL,0,0,'2025-05-31 08:39:29',1),(28180029,'don_mathan','Mathan kumar amalraj',NULL,0,0,'2025-05-31 13:40:00',1),(28207436,'TweetsfromArun','Dr.டேய் தம்பி உன்னை தான் டா 4.o?',NULL,0,0,'2025-06-01 02:18:11',1),(28230307,'tweeterPill','Kaari Maran',NULL,0,0,'2025-06-01 12:36:28',1),(28234771,'KarunyanMBA','Karunyan MBA',NULL,0,0,'2025-06-01 14:30:53',1),(28249181,'agskumar5','?? ??⚔️',NULL,0,0,'2025-06-01 20:48:35',1),(28278631,'laksh7t','?????',NULL,0,0,'2025-06-02 09:26:45',0),(28280402,'DMK_for_Life_','Chennai Paiyan ?❤️',NULL,0,0,'2025-06-02 10:30:23',0),(28281470,'DhanasekaranGN','Dhanasekaran',NULL,0,0,'2025-06-02 11:08:15',1),(28284595,'maaran_pandi','மாறன் பாண்டியன்',NULL,0,0,'2025-06-02 12:59:19',1),(28285525,'Yaazhavel','யாழவன்',NULL,0,0,'2025-06-02 13:30:35',0),(28288282,'koltikumar18973','இட்டாச்சி உச்சிகா',NULL,0,0,'2025-06-02 15:39:18',0),(28289315,'World_Tamils1','உலகத்தமிழர்',NULL,0,0,'2025-06-02 16:10:50',0),(28289952,'SanthoshinX','Santhosh Sakthi',NULL,0,0,'2025-06-02 16:34:01',0),(28291858,'tbstamilnadu','The Black Spectacle',NULL,0,0,'2025-06-02 17:37:28',1),(28298014,'Sandy150919','Sandy',NULL,0,0,'2025-06-02 21:09:49',1),(28300426,'TamilBeats4U','TamilBeats4U?',NULL,0,0,'2025-06-02 22:32:35',0),(28308731,'AbdulBoys478831','Sᴘɪᴅᴇʀ ᴍᴀɴ ?',NULL,0,0,'2025-06-03 03:08:48',0),(28309060,'miltonrabo45787','ஈழச் சாரல்',NULL,0,0,'2025-06-03 03:19:32',0),(28317567,'nothing_illai','Thanos☣️',NULL,0,0,'2025-06-03 08:05:22',0),(28319689,'siva_mojo','SIVAMAYA?',NULL,0,0,'2025-06-03 09:17:32',0),(28322580,'SilverBack484','Saul Goodman',NULL,0,0,'2025-06-03 10:54:39',0),(28324988,'JK_Kshama6666','JK',NULL,0,0,'2025-06-03 12:14:08',0),(28326043,'_AngelKD','இவள் தமிழ் தேவதை',NULL,0,0,'2025-06-03 12:50:09',0),(28327217,'winning4sure','premamkumar',NULL,0,0,'2025-06-03 13:28:48',0),(28329607,'nandhaninam','K P கருப்பு',NULL,0,0,'2025-06-03 14:48:09',0),(28329709,'iamtitanoboa','ᴰᵃᵈʸ?????',NULL,0,0,'2025-06-03 14:51:57',0),(28331006,'being_shudra','மோக்லீ',NULL,0,0,'2025-06-03 15:36:00',0),(28331708,'TheIceMaster07','iceman❄️❄️',NULL,0,0,'2025-06-03 15:59:18',0),(28331896,'THALArasigaiii','????? ??? ???? ♡',NULL,0,0,'2025-06-03 16:05:36',0),(28345337,'i_little_hearts','??????',NULL,0,0,'2025-06-03 23:46:06',0),(28347844,'hems90_r','ஹேமா?✨',NULL,0,0,'2025-06-04 01:13:13',0),(28348206,'MuhilThalaiva','Mᴜʜɪʟツ?',NULL,0,0,'2025-06-04 01:26:23',0),(28349027,'smileyboyoff','S M I L E Y',NULL,0,0,'2025-06-04 01:51:43',0),(28358451,'bk_bites0319','тαмιℓραιуєи?️',NULL,0,0,'2025-06-04 07:11:56',0),(28359777,'TvkLeo2024','??? ????',NULL,0,0,'2025-06-04 07:55:25',0),(28364375,'majaamaa','మஜா',NULL,0,0,'2025-06-04 10:33:00',0),(28365392,'drcnpkaran1','Naveen Prabakaran',NULL,0,0,'2025-06-04 11:05:41',0),(28366358,'Mamtha_Offcl','✨Mamtha?Priya✨',NULL,0,0,'2025-06-04 11:37:38',0),(28367124,'iraiyon_1609','?????? ???????✍️',NULL,0,0,'2025-06-04 12:03:40',0),(28368782,'Siva_4991','Mr.S',NULL,0,0,'2025-06-04 12:56:16',0),(28369193,'Thz_Jack_JD','???? ??',NULL,0,0,'2025-06-04 13:10:16',0),(28370236,'k_kadi_korangu','ஆலன் குரங்கு',NULL,0,0,'2025-06-04 13:43:59',0),(28371298,'lekhsoffl','Demon Lekha ?',NULL,0,0,'2025-06-04 14:18:30',0),(28373305,'Incredib_Hulk','Hulk',NULL,0,0,'2025-06-04 15:23:56',0),(28374119,'Ayyappan_1504','Ayyappan',NULL,0,0,'2025-06-04 15:50:31',0),(28374158,'itz_Dilip','Dilip',NULL,0,0,'2025-06-04 15:51:48',0),(28374531,'Doctor_Doktor','??. ????????',NULL,0,0,'2025-06-04 16:05:04',0);
/*!40000 ALTER TABLE `Following` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Settings`
--

DROP TABLE IF EXISTS `Settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Settings` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Value` text NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Settings`
--

LOCK TABLES `Settings` WRITE;
/*!40000 ALTER TABLE `Settings` DISABLE KEYS */;
INSERT INTO `Settings` VALUES (1,'DataRefresh','150001'),(2,'UIRefresh','300000'),(3,'CardAvgRefresh','5000'),(6,'StatusRefresh','30000'),(7,'RecordArguments','-i {AudioLink} -c:v libx265 -crf 28 -c:a aac -b:a 128k -f segment -segment_time 1800 -reset_timestamps 1 -map 0 -segment_format_options movflags=+faststart \"{RecFolder}/Space_{SpaceId}_{DateTimeNow}-%03d.mp4\"'),(8,'WatcherRefresh','60000'),(9,'ReadTweetUrl','https://x.com/i/api/graphql/dh2lDmjqEkxCWQK_UxkH4w/UserTweets?variables=%7B%22userId%22%3A%221723022012052881408%22%2C%22count%22%3A20%2C%22cursor%22%3A%22DAABCgABGA7CgyL___sIAAMAAAACAAA%22%2C%22includePromotedContent%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_home_pinned_timelines_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'),(10,'Ntags','UnUsed #XSpacesOnline'),(11,'CreateTweetPath','zIdRTsSqcD6R5uMtm_N0pw'),(12,'AddFollowerNewHosts','1'),(13,'DeleteFollowingInActiveMonths','6'),(14,'TelegramChatID','-1002320238035'),(15,'TelegramBotToken','7209651290:AAGryM8xz2i6xMx3BsDOQCDdVB4leBl39Dw'),(16,'TelegramUrl','https://api.telegram.org/bot7209651290:AAGryM8xz2i6xMx3BsDOQCDdVB4leBl39Dw/sendMessage?chat_id=-1002221143419&text={message}');
/*!40000 ALTER TABLE `Settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TSEServices`
--

DROP TABLE IF EXISTS `TSEServices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TSEServices` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ServiceName` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TSEServices`
--

LOCK TABLES `TSEServices` WRITE;
/*!40000 ALTER TABLE `TSEServices` DISABLE KEYS */;
INSERT INTO `TSEServices` VALUES (1,'TSE.Discovery'),(2,'TSE.Discovery.Status'),(3,'TSE.Discovery.Watcher');
/*!40000 ALTER TABLE `TSEServices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TwitterSpacesMain`
--

DROP TABLE IF EXISTS `TwitterSpacesMain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TwitterSpacesMain` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `SpaceUrl` varchar(100) DEFAULT NULL,
  `HostName` varchar(100) DEFAULT NULL,
  `M3U8Url` varchar(1500) DEFAULT NULL,
  `SpaceTitle` varchar(1000) DEFAULT NULL,
  `HostDisplayName` varchar(500) DEFAULT NULL,
  `StartDateTime` datetime DEFAULT NULL,
  `IsRecording` tinyint(1) DEFAULT NULL,
  `IsListening` tinyint(1) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `IsHost` tinyint(1) DEFAULT NULL,
  `SpaceType` varchar(100) DEFAULT NULL,
  `UserName` varchar(50) DEFAULT NULL,
  `DisplayName` varchar(50) DEFAULT NULL,
  `bAutoRecord` int(11) DEFAULT NULL,
  `SpeakerCount` int(11) DEFAULT NULL,
  `HostCount` int(11) DEFAULT NULL,
  `LastActivity` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `unique_space_key` (`SpaceUrl`,`HostName`)
) ENGINE=InnoDB AUTO_INCREMENT=1493647 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TwitterSpacesMain`
--

LOCK TABLES `TwitterSpacesMain` WRITE;
/*!40000 ALTER TABLE `TwitterSpacesMain` DISABLE KEYS */;
/*!40000 ALTER TABLE `TwitterSpacesMain` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-04 20:03:22
