CREATE TABLE `posts` (
  `id` varchar(100) NOT NULL,
  `caption` longtext,
  `picture_url` varchar(255) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `pos` double DEFAULT NULL,
  `neu` double DEFAULT NULL,
  `neg` double DEFAULT NULL,
  PRIMARY KEY (`id`,`picture_url`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
