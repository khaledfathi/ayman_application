DROP TABLE  IF EXISTS  `ayman`.`orders`;

CREATE TABLE `ayman`.`orders`(
`id` INT(6) AUTO_INCREMENT PRIMARY KEY ,
`name` VARCHAR(50) CHARSET utf8,
`address` VARCHAR(255) CHARSET utf8,
`phone` VARCHAR(50) CHARSET utf8,
`cities` VARCHAR(50) CHARSET utf8 ,
`product_type`TEXT CHARSET utf8,
`product_link`TEXT CHARSET utf8,
`pic_file` TEXT CHARSET utf8,
`pic_url` TEXT CHARSET utf8,
`request_date` DATE,
`end_date` DATE ,
`email`	VARCHAR(50) CHARSET utf8,
`souq_password` VARCHAR(50) CHARSET utf8,
`request_status` VARCHAR(50) CHARSET utf8,
`tracking_link` TEXT CHARSET utf8,
`notes` TEXT CHARSET utf8
);
