-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: fireflyapp-db-firefly-3ba2.j.aivencloud.com:18245
-- Generation Time: Jul 30, 2026 at 07:11 AM
-- Server version: 8.0.45
-- PHP Version: 8.5.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `defaultdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `Following`
--

CREATE TABLE `Following` (
  `ID` bigint NOT NULL,
  `UserName` varchar(100) NOT NULL,
  `DisplayName` varchar(200) DEFAULT NULL,
  `bAutoRecord` tinyint(1) DEFAULT NULL,
  `SpeakerCount` int DEFAULT '0',
  `HostCount` int DEFAULT '0',
  `LastActivity` datetime DEFAULT NULL,
  `MainUser` int DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Following`
--

INSERT INTO `Following` (`ID`, `UserName`, `DisplayName`, `bAutoRecord`, `SpeakerCount`, `HostCount`, `LastActivity`, `MainUser`) VALUES
(1, 'bala1422578', '🪔பாலா🪔', NULL, 0, 0, NULL, 1),
(2, 'thodaadha', 'தொடாத', NULL, 0, 0, NULL, 1),
(3, 'KarthiK14564977', '𝖐𝖆𝖗𝖙𝖍𝖎🤍 𝖐𝖊y𝖆𝖓', NULL, 0, 0, NULL, 1),
(4, 'palasudharsan_m', 'பாலசுதர்சன் முத்துராஜ்', NULL, 0, 0, NULL, 1),
(5, 'EURONGREYJOY007', 'Dr. 2G Spectrum 🍇 💰', NULL, 0, 0, NULL, 1),
(6, 'NagaS8800', 'laxmi.s', NULL, 0, 0, NULL, 1),
(9, 'TvkCafeHQ', 'TVK CAFE HQ', NULL, 0, 0, NULL, 1),
(10, 'samooham', 'TVKBLAST', NULL, 0, 0, NULL, 1),
(11, 'Pavithra03V', 'Makeup Artist', NULL, 0, 0, NULL, 1),
(12, 'muthurajvembu', 'Muthuraj', NULL, 0, 0, NULL, 1),
(13, 'Manirosyajay', 'செ. மணிகண்டன்', NULL, 0, 0, NULL, 1),
(14, 'Vadirocks', 'Varunn', NULL, 0, 0, NULL, 1),
(15, 'iGPS003', 'GPS', NULL, 0, 0, NULL, 1),
(16, 'NShamsuthin', 'Shamsuthin umar', NULL, 0, 0, NULL, 1),
(17, 'offlThangaraj', 'தங்கராசு வேலு', NULL, 0, 0, NULL, 1),
(18, 'Sheik_tn9', '🤙Mannai☀', NULL, 0, 0, NULL, 1),
(21, 'Murali8493', 'முரளி VJ', NULL, 0, 0, NULL, 1),
(22, 'SadistXOX', 'Entertainment & Recreation', NULL, 0, 0, NULL, 1),
(23, 'DhanasekaranGN', 'Dhanasekaran', NULL, 0, 0, NULL, 1),
(24, 'Tamizh_Vendhar', 'தமிழ்வேந்தர்', NULL, 0, 0, NULL, 1),
(25, 'Velmuru51716413', 'Velmurugan', NULL, 0, 0, NULL, 1),
(26, 'PrakashMahadev', 'Prakash Mahadevan', NULL, 0, 0, NULL, 1),
(27, 'sureshlal', '🇮🇳Suresh लाल #தருமி🇮🇳', NULL, 0, 0, NULL, 1),
(29, 'all4shiro', 'Shiro', NULL, 0, 0, NULL, 1),
(30, 'Kani_Rabi143', '𝑯𝒂𝒏𝒊𝒇𝒂💫', NULL, 0, 0, NULL, 1),
(33, 'imswarroom6', 'Psephologist IMS2.0', NULL, 0, 0, NULL, 1),
(34, 'Djagannathan1', 'காந்தி#இளையராஜா#மோடி#அண்ணாமலை', NULL, 0, 0, NULL, 1),
(35, 'Common__Voice', 'RDP', NULL, 0, 0, NULL, 1),
(37, 'seelanano', 'இராவணன்', NULL, 0, 0, NULL, 1),
(40, 'PasteHere', 'Paste Here', NULL, 0, 0, NULL, 1),
(41, 'nallalavaruman', 'நல்லாளவருமன்', NULL, 0, 0, NULL, 1),
(42, 'LeagueRed58401', 'ISKRA', NULL, 0, 0, NULL, 1),
(45, 'Karthikravivarm', 'Karthik Ravivarma', NULL, 0, 0, NULL, 1),
(47, 'JesusAlexaande1', 'அருணாசலம்', NULL, 0, 0, NULL, 1),
(49, 'triplephd', 'AsTro Hakuna 🇮🇳', NULL, 0, 0, NULL, 1),
(70, 'Rajini12Dhoni7', 'என்றும் தலைவர் ரசிகன்ᴶᴬᴵᴸᴱᴿ💛', NULL, 0, 0, NULL, 1),
(73, 'SakthiV93833759', 'சக்தி வேல்💥_தமிழன்', NULL, 0, 0, NULL, 1),
(74, '_peacemaker07_', 'Entertainment & Recreation', NULL, 0, 0, NULL, 1),
(88, 'thattampoochi', 'தட்டான் பூச்சி', NULL, 0, 0, NULL, 1),
(89, 'pidisambal', 'பிடிசாம்பல்', NULL, 0, 0, NULL, 1),
(105, 'on_struggle', 'keepmoving on struggle', NULL, 0, 0, NULL, 1),
(109, 'Jana_Naayagan', 'Mʀ.Exᴘɪʀʏ', NULL, 0, 0, NULL, 1),
(112, 'Kokki_Boys', 'Intellectual', NULL, 0, 0, NULL, 1),
(117, 'E_quality_5ter', 'Entertainment & Recreation', NULL, 0, 0, NULL, 1),
(119, 'ItsKeeran', 'Keeran', NULL, 0, 0, NULL, 1),
(120, 'kajan1215', 'கரன்', NULL, 0, 0, NULL, 1),
(121, 'enigma_timorous', 'Timorous Enigma', NULL, 0, 0, NULL, 1),
(127, 'DravidTvk', 'Entertainment & Recreation', NULL, 0, 0, NULL, 1),
(137, 'Ondragaofficial', 'Ondraga', NULL, 0, 0, NULL, 1),
(141, 'JDALEXtweets', 'ʲᵈᴀʟᴇxᴀɴᴅᴇʀᵗʷᵉᵉᵗˢ', NULL, 0, 0, NULL, 1),
(149, 'musthafa901', 'முஸ்து', NULL, 0, 0, NULL, 1),
(183, 'rawdyiyer', 'ஐயர்லயே நான் ஒரு மாதிரியாக்கும்', NULL, 0, 0, NULL, 1),
(339, 'Rajasakthim', 'Public & Social Services', NULL, 0, 0, NULL, 1),
(340, 'iycmahe', 'Media Personality', NULL, 0, 0, NULL, 1),
(364, 'VigneShVijayjos', 'VigneSh Vijay தவெக', NULL, 0, 0, NULL, 1),
(365, 'marketforce10', 'Advertising & Marketing Agency', NULL, 0, 0, NULL, 1),
(366, 'JDave1981', 'Jay', NULL, 0, 0, NULL, 1),
(388, 'H_a_r_r_y_95', '🅷🅰🆁🆁🆈', NULL, 0, 0, NULL, 1),
(389, 'Archunaaa', 'Arjun Raja Raja Perum Paraiyar', NULL, 0, 0, NULL, 1),
(392, 'prabu_bala85', 'பிரபு பாலா', NULL, 0, 0, NULL, 1),
(393, 'Ranjith_Rayappa', 'Black Panther', NULL, 0, 0, NULL, 1),
(397, 'Chandrumlpt', 'ABD', NULL, 0, 0, NULL, 1),
(398, 'trendinglanka', 'Software Application', NULL, 0, 0, NULL, 1),
(399, 'VIKRAM734523767', 'VIKRAM- VOTE FOR TVK', NULL, 0, 0, NULL, 1),
(400, 'kumarisoil', 'குமரி மண்', NULL, 0, 0, NULL, 1),
(401, 'iamtitanoboa', 'Entertainment & Recreation', NULL, 0, 0, NULL, 1),
(407, 'birla2345', 'birla 2345', NULL, 0, 0, NULL, 1),
(432, 'Karthickrames1', 'Stand With Savukku', NULL, 0, 0, NULL, 1),
(435, 'robin94_tvk', 'Robin', NULL, 0, 0, NULL, 1),
(455, 'RR013C', 'KaWin', NULL, 0, 0, NULL, 1),
(659, 'i_am_paavendhan', 'பாவேந்தன்', NULL, 0, 0, NULL, 1),
(664, 'aalanpangali', 'ஆலன் பங்காளி (AK)', NULL, 0, 0, NULL, 1),
(665, 'ArunRose_100', 'தங்கமகன் 100', NULL, 0, 0, NULL, 1),
(777, 'Civilerbala1979', 'Balamurugan', NULL, 0, 0, NULL, 1),
(803, 'pandiyah1', 'Cockroach Parti', NULL, 0, 0, NULL, 1),
(804, 'xAI_Avatar', 'Avatar', NULL, 0, 0, NULL, 1),
(806, 'RoiEelam', 'அரசன்', NULL, 0, 0, NULL, 1),
(823, 'mazhaisara', 'மழை சாரல்', NULL, 0, 0, NULL, 1),
(824, 'Minerva492156', 'Accountant', NULL, 0, 0, NULL, 1),
(826, 'dravidan_1925', 'திராவிடன் ( Bruce Wayne )', NULL, 0, 0, NULL, 1),
(838, 'Karthicktntvl', 'Tιρʂ', NULL, 0, 0, NULL, 1),
(839, 'dharmic_indians', 'Non-Governmental & Nonprofit Organization ', NULL, 0, 0, NULL, 1),
(871, 'sarvaadhikari', 'சர்வாதிகாரி', NULL, 0, 0, NULL, 1),
(876, 'keeramundai', 'சொட்டசுமோ_கெட்டசுமோ', NULL, 0, 0, NULL, 1),
(877, 'Rollercaster123', 'Saul Goodman', NULL, 0, 0, NULL, 1),
(878, 'Rajkumar4530703', 'RajkumarTNLIST', NULL, 0, 0, NULL, 1),
(879, 'Ravimahesh31157', 'krishna', NULL, 0, 0, NULL, 1),
(955, 'jillasudhakar01', '_.jilla.sudhakar._', NULL, 0, 0, NULL, 1),
(963, '___Maran', 'மாran', NULL, 0, 0, NULL, 1),
(967, 'odakkon', 'போர்க்குடி வண்ணார்', NULL, 0, 0, NULL, 1),
(975, 'dhalifofficial', 'M Dhalif', NULL, 0, 0, NULL, 1),
(994, 'machi199090', 'மச்சி', NULL, 0, 0, NULL, 1),
(1011, 'akajithkumar463', 'Hulk man', NULL, 0, 0, NULL, 1),
(1032, 'DSalltvk', 'Endrick DS', NULL, 0, 0, NULL, 1),
(1150, 'Razorblack_', 'Razor Black', NULL, 0, 0, NULL, 1),
(1172, 'its_me__vijay', '𝄞ரிதம்💫', NULL, 0, 0, NULL, 1),
(1220, 'Common_man_ak', 'Proletarian_Left☭', NULL, 0, 0, NULL, 1),
(1222, 'iMariaJuliana', 'Entertainment & Recreation', NULL, 0, 0, NULL, 1),
(1277, 'ADMK_Trends', 'ADMK Trends🌱✌️ ❤️ Say No To Drugs & DMK', NULL, 0, 0, NULL, 1),
(1278, 'vasloga', '𝗟𝗼𝗴𝗮𝗻♬', NULL, 0, 0, NULL, 1),
(1279, 'shaanshantha', 'Shaan🤍', NULL, 0, 0, NULL, 1),
(1331, 'ppugazhmpp', 'Entertainment & Recreation', NULL, 0, 0, NULL, 1),
(1332, 'vanni_1991', 'Vino⚡️', NULL, 0, 0, NULL, 1),
(1339, '_ImVasu', 'Koduva ADMK :)', NULL, 0, 0, NULL, 1),
(1341, 'Akashraavanan15', 'Public & Social Services', NULL, 0, 0, NULL, 1),
(1384, 'agskumar5', '𝐌𝐫 𝐨𝐡⚔️', NULL, 0, 0, NULL, 1),
(1408, 'Huggy_shan_619', 'Entrepreneur', NULL, 0, 0, NULL, 1),
(1477, 'karm39am', 'Lakshmi vijayan', NULL, 0, 0, NULL, 1),
(1547, 'rojaPeriyarist', 'Roja', NULL, 0, 0, NULL, 1),
(1563, 'fearlessfalconw', 'அனு ✨⚛️⚛️✨', NULL, 0, 0, NULL, 1),
(1564, 'charmfulGrace', ' CL ', NULL, 0, 0, NULL, 1),
(1567, 'Kadapparaiboys', 'கடப்பாரை', NULL, 0, 0, NULL, 1),
(1605, 'Periambed15', 'S K', NULL, 0, 0, NULL, 1),
(1633, 'john3m5g', 'BLACK&RED', NULL, 0, 0, NULL, 1),
(1644, 'burnitwithblue', 'Avarna கலகக்காரன்', NULL, 0, 0, NULL, 1),
(1650, 'kabali2022', 'மாட்டு பால்', NULL, 0, 0, NULL, 1),
(1651, 'SydneyTamilan', 'Sydney Tamilan', NULL, 0, 0, NULL, 0),
(1652, 'itz_khadeeja', 'khadeeja 💕', NULL, 0, 0, NULL, 0),
(1653, 'nil427408064892', '🌜நிலா🌛', NULL, 0, 0, NULL, 0),
(1654, 'Balal0c', 'பாலா', NULL, 0, 0, NULL, 0),
(1655, 'AsiKv12', NULL, NULL, 0, 0, NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `Settings`
--

CREATE TABLE `Settings` (
  `ID` int NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Value` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Settings`
--

INSERT INTO `Settings` (`ID`, `Name`, `Value`) VALUES
(1, 'DataRefresh', '150001'),
(2, 'UIRefresh', '300000'),
(3, 'CardAvgRefresh', '5000'),
(6, 'StatusRefresh', '30000'),
(7, 'RecordArguments', '-i {AudioLink} -c:v libx265 -crf 28 -c:a aac -b:a 128k -f segment -segment_time 1800 -reset_timestamps 1 -map 0 -segment_format_options movflags=+faststart \"{RecFolder}/Space_{SpaceId}_{DateTimeNow}-%03d.mp4\"'),
(8, 'WatcherRefresh', '60000'),
(9, 'ReadTweetUrl', 'https://x.com/i/api/graphql/dh2lDmjqEkxCWQK_UxkH4w/UserTweets?variables=%7B%22userId%22%3A%221723022012052881408%22%2C%22count%22%3A20%2C%22cursor%22%3A%22DAABCgABGA7CgyL___sIAAMAAAACAAA%22%2C%22includePromotedContent%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_home_pinned_timelines_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'),
(10, 'Ntags', 'UnUsed #XSpacesOnline'),
(11, 'CreateTweetPath', 'zIdRTsSqcD6R5uMtm_N0pw'),
(12, 'AddFollowerNewHosts', '1'),
(13, 'DeleteFollowingInActiveMonths', '6'),
(14, 'TelegramChatID', '-1002726876695'),
(15, 'TelegramBotToken', '8390103076:AAF9Xd3jMLJLEhA4PCfe7fN_5ECdUedTCUA'),
(16, 'TelegramUrl', 'https://api.telegram.org/bot8390103076:AAF9Xd3jMLJLEhA4PCfe7fN_5ECdUedTCUA/sendMessage?chat_id=-1002726876695&text={message}'),
(17, 'DiscordWebhookURL', 'https://discord.com/api/webhooks/1504587790082375743/ypJJS9Ojb09MH9e40PHfuw-J2Flpo-DgxBRnHuuZHsdfuWchezDYjrN5uD9JDOudgZHD');

-- --------------------------------------------------------

--
-- Table structure for table `TSEServices`
--

CREATE TABLE `TSEServices` (
  `ID` int NOT NULL,
  `ServiceName` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `TSEServices`
--

INSERT INTO `TSEServices` (`ID`, `ServiceName`) VALUES
(1, 'TSE.Discovery'),
(2, 'TSE.Discovery.Status'),
(3, 'TSE.Discovery.Watcher');

-- --------------------------------------------------------

--
-- Table structure for table `TwitterSpacesMain`
--

CREATE TABLE `TwitterSpacesMain` (
  `ID` bigint NOT NULL,
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
  `bAutoRecord` int DEFAULT NULL,
  `SpeakerCount` int DEFAULT NULL,
  `HostCount` int DEFAULT NULL,
  `LastActivity` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Following`
--
ALTER TABLE `Following`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `idx_username` (`UserName`),
  ADD UNIQUE KEY `uniq_username` (`UserName`);

--
-- Indexes for table `Settings`
--
ALTER TABLE `Settings`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `TSEServices`
--
ALTER TABLE `TSEServices`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `TwitterSpacesMain`
--
ALTER TABLE `TwitterSpacesMain`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `unique_space_key` (`SpaceUrl`,`HostName`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Following`
--
ALTER TABLE `Following`
  MODIFY `ID` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2110;

--
-- AUTO_INCREMENT for table `Settings`
--
ALTER TABLE `Settings`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `TSEServices`
--
ALTER TABLE `TSEServices`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `TwitterSpacesMain`
--
ALTER TABLE `TwitterSpacesMain`
  MODIFY `ID` bigint NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
