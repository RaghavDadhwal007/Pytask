DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
);

DROP TABLE IF EXISTS `addresses`;

CREATE TABLE `addresses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `street` varchar(255) NOT NULL,
  `pincode` int NOT NULL,
  `country` varchar(20) NOT NULL,
  `state` varchar(20) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_User` (`user_id`),
  CONSTRAINT `FK_User` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
);
