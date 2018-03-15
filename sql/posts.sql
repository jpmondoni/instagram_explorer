CREATE TABLE `posts` (
	`id` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_bin',
	`caption` LONGTEXT NULL COLLATE 'utf8mb4_bin',
	`picture_url` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_bin',
	`timestamp` INT(11) NOT NULL,
	`pos` DOUBLE NULL DEFAULT NULL,
	`neu` DOUBLE NULL DEFAULT NULL,
	`neg` DOUBLE NULL DEFAULT NULL,
	`hashtag` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_bin',
	PRIMARY KEY (`id`)
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB
;
