CREATE TABLE `insights` (
	`post_id` VARCHAR(50) NULL DEFAULT NULL,
	`dominant_color` VARCHAR(7) NULL DEFAULT NULL,
	`avg_color` VARCHAR(7) NULL DEFAULT NULL,
	`peak` VARCHAR(255) NULL DEFAULT NULL,
	UNIQUE INDEX `post_id` (`post_id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;
