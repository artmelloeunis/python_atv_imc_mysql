CREATE DATABASE `imc`;

USE `imc`;

DROP TABLE IF EXISTS `imc`;

CREATE TABLE `imc` (
  `id` int NOT NULL AUTO_INCREMENT,
  `paciente` varchar(100) DEFAULT NULL,
  `endereco` varchar(100) DEFAULT NULL,
  `altura` float DEFAULT NULL,
  `peso` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
