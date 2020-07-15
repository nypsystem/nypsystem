DROP DATABASE IF EXISTS systemsecurity;
CREATE DATABASE IF NOT EXISTS systemsecurity;
USE systemsecurity;
DROP TABLE IF EXISTS Accounts;
CREATE TABLE IF NOT EXISTS Accounts (
id int NOT NULL AUTO_INCREMENT,
username varchar(50) NOT NULL,
password varchar(255) NOT NULL,
email varchar(255) NOT NULL,
symmetrickey varchar(255) NULL,
mobile varchar(255) NOT NULL,
admin int NULL,
 PRIMARY KEY (id)
)ENGINE=InnoDB AUTO_INCREMENT=2;
INSERT INTO `systemsecurity`.`accounts`
(`username`,`password`,`email`,`symmetrickey`,`mobile`,`admin`)
VALUES
('test','$2b$16$nCDwqm3gs4Yaetq06pzhy.TGD9C3H52Xt50cRneRjcjZ8Oj6XiTRq','gAAAAABfCpXo-AJcLM8DjVBf1VAaPULtMnEAw_R8NMabM0cItqxcaOREjK8XIBH4zS67jxZ32Jc7ZJwjpHXywLQPf6vHQDs_Yg==','c6QEunBBsV5Yq_Mnrw1z2AUuC-FFGUzelf1fL07PmPM=','gAAAAABfCpXoArCogoh04e5zMCnE1zIUsLzSofMEoZ_w6Fm0YE4BMA6zOxe6cH-kHXmfpAU9cKic0Z-WIqXg0E10AID49zvnOw==','1');