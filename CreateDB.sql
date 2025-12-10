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
(16, 'TelegramUrl', 'https://api.telegram.org/bot8390103076:AAF9Xd3jMLJLEhA4PCfe7fN_5ECdUedTCUA/sendMessage?chat_id=-1002726876695&text={message}');

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
