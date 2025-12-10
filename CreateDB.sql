DROP TABLE IF EXISTS `TwitterSpacesMain`;
DROP TABLE IF EXISTS `TSEServices`;
DROP TABLE IF EXISTS `Settings`;
DROP TABLE IF EXISTS `Following`;

-- =========================================
-- Following
-- =========================================
CREATE TABLE `Following` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `UserName` varchar(100) NOT NULL,
  `DisplayName` varchar(200) DEFAULT NULL,
  `bAutoRecord` tinyint(1) DEFAULT NULL,
  `SpeakerCount` int(11) DEFAULT '0',
  `HostCount` int(11) DEFAULT '0',
  `LastActivity` datetime DEFAULT NULL,
  `MainUser` int(11) DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `idx_username` (`UserName`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

INSERT INTO `Following` (`ID`, `UserName`, `DisplayName`, `bAutoRecord`, `SpeakerCount`, `HostCount`, `LastActivity`, `MainUser`) VALUES
(1, 'JDave1981', 'Jay', NULL, 0, 0, NULL, 1),
(2, 'dravidan_1925', 'திராவிடன்', NULL, 0, 0, NULL, 1),
(3, 'thil_sek', 'Dr.Thillli PhD 🎷🧬🎸🧬🎺🧬🎤🧬🥁🧬', NULL, 0, 0, NULL, 1),
(4, 'chennaiweather', 'Chennai Weather-Raja', NULL, 0, 0, NULL, 0),
(5, 'elonmusk', 'Elon Musk', NULL, 0, 0, NULL, 0),
(6, 'all4shiro', 'Shiro', NULL, 0, 0, NULL, 0);

-- =========================================
-- Settings
-- =========================================
CREATE TABLE `Settings` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Value` text NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;

INSERT INTO `Settings` (`ID`, `Name`, `Value`) VALUES
(1, 'DataRefresh', '150001'),
(2, 'UIRefresh', '300000'),
(3, 'CardAvgRefresh', '5000'),
(4, 'StatusRefresh', '30000'),
(5, 'RecordArguments', '-i ...'),
(6, 'WatcherRefresh', '60000'),
(7, 'ReadTweetUrl', 'https://x.com/...'),
(8, 'Ntags', 'UnUsed #XSpacesOnline'),
(9, 'CreateTweetPath', 'zIdRTsSqcD6R5uMtm_N0pw'),
(10, 'AddFollowerNewHosts', '1'),
(11, 'DeleteFollowingInActiveMonths', '6'),
(12, 'TelegramChatID', '-1002726876695'),
(13, 'TelegramBotToken', 'REDACTED'),
(14, 'TelegramUrl', 'REDACTED');

-- =========================================
-- TSEServices
-- =========================================
CREATE TABLE `TSEServices` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ServiceName` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

INSERT INTO `TSEServices` (`ID`, `ServiceName`) VALUES
(1, 'TSE.Discovery'),
(2, 'TSE.Discovery.Status'),
(3, 'TSE.Discovery.Watcher');

-- =========================================
-- TwitterSpacesMain
-- =========================================
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

COMMIT;
