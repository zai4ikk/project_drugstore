CREATE DATABASE drugstore;

USE drugstore;

-- Хранимая процедура для хэширования пароля
DELIMITER //
CREATE PROCEDURE HashPassword (IN inputPassword VARCHAR(255), OUT hashedPassword VARCHAR(255))
BEGIN
    SET hashedPassword = SHA2(inputPassword, 256);
END //
DELIMITER ;

-- Таблица назначений лекарств
CREATE TABLE IF NOT EXISTS `assignationmedicament` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Groupmedicament` VARCHAR(25) NULL DEFAULT NULL,
  `Description` TEXT NULL DEFAULT NULL,
  `Image` VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- Таблица клиентов
CREATE TABLE IF NOT EXISTS `client` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(50) NULL DEFAULT NULL,
  `Login` VARCHAR(50) NOT NULL UNIQUE,
  `Password` VARCHAR(255) NOT NULL,
  `Representative` VARCHAR(50) NULL DEFAULT NULL,
  `Adress` TEXT NULL DEFAULT NULL,
  `Phonenumber` VARCHAR(15) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
);

-- Таблица болезней
CREATE TABLE IF NOT EXISTS `diseases` (
  `Illness` VARCHAR(255) NULL DEFAULT NULL,
  `IDAssignationmedicament` INT NULL DEFAULT NULL
);

-- Таблица сотрудников
CREATE TABLE IF NOT EXISTS `employee` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Fullname` VARCHAR(50) NULL DEFAULT NULL,
  `Post` VARCHAR(50) NULL DEFAULT NULL,
  `Login` VARCHAR(50) NOT NULL UNIQUE,
  `Password` VARCHAR(255) NOT NULL,
  `Birthdate` DATE NULL DEFAULT NULL,
  `Dateofhiring` DATE NULL DEFAULT NULL,
  `Phonenumber` VARCHAR(15) NOT NULL UNIQUE,
  `Photo` VARCHAR(50) NULL DEFAULT NULL,
  `Education` VARCHAR(50) NULL DEFAULT NULL,
  `Salary` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- Таблица медикаментов
CREATE TABLE IF NOT EXISTS `medicament` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(50) NULL DEFAULT NULL,
  `IDAssignationmedicament` INT NULL DEFAULT NULL,
  `IDProvider` INT NULL DEFAULT NULL,
  `Unitsofmeasurement` VARCHAR(50) NULL DEFAULT NULL,
  `Pricepurchase` DECIMAL(10,2) NULL DEFAULT NULL,
  `Pricerealization` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- Таблица заказанных товаров
CREATE TABLE IF NOT EXISTS `ordered` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `IDMedicament` INT NULL DEFAULT NULL,
  `IDOrders` INT NULL DEFAULT NULL,
  `Pricerealization` DECIMAL(10,2) NULL DEFAULT NULL,
  `Quantity` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- Таблица заказов
CREATE TABLE IF NOT EXISTS `orders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `IDClient` INT NULL DEFAULT NULL,
  `IDEmployee` INT NULL DEFAULT NULL,
  `Dateofplacement` DATE NULL DEFAULT NULL,
  `Dateappointment` DATE NULL DEFAULT NULL,
  `Dateperformance` DATE NULL DEFAULT NULL,
  `Deliverycost` DECIMAL(10,2) NULL DEFAULT NULL,
  `Recipient` VARCHAR(50) NULL DEFAULT NULL,
  `Recipientaddress` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- Таблица поставщиков
CREATE TABLE IF NOT EXISTS `provider` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(50) NULL DEFAULT NULL,
  `Representative` VARCHAR(50) NULL DEFAULT NULL,
  `Post` VARCHAR(50) NULL DEFAULT NULL,
  `Phonenumber` VARCHAR(15) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
);

-- Таблица администраторов
CREATE TABLE IF NOT EXISTS `administrator` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Fullname` VARCHAR(50) NOT NULL,
  `Login` VARCHAR(50) NOT NULL UNIQUE,
  `Password` VARCHAR(255) NOT NULL,
  `Phonenumber` VARCHAR(15) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
);

-- Триггеры для хэширования паролей перед вставкой и обновлением в таблицах клиентов, сотрудников и администраторов
DELIMITER //

CREATE TRIGGER before_client_insert
BEFORE INSERT ON client
FOR EACH ROW
BEGIN
    CALL HashPassword(NEW.Password, @hashedPassword);
    SET NEW.Password = @hashedPassword;
END //

CREATE TRIGGER before_client_update
BEFORE UPDATE ON client
FOR EACH ROW
BEGIN
    CALL HashPassword(NEW.Password, @hashedPassword);
    SET NEW.Password = @hashedPassword;
END //

CREATE TRIGGER before_employee_insert
BEFORE INSERT ON employee
FOR EACH ROW
BEGIN
    CALL HashPassword(NEW.Password, @hashedPassword);
    SET NEW.Password = @hashedPassword;
END //

CREATE TRIGGER before_employee_update
BEFORE UPDATE ON employee
FOR EACH ROW
BEGIN
    CALL HashPassword(NEW.Password, @hashedPassword);
    SET NEW.Password = @hashedPassword;
END //

CREATE TRIGGER before_administrator_insert
BEFORE INSERT ON administrator
FOR EACH ROW
BEGIN
    CALL HashPassword(NEW.Password, @hashedPassword);
    SET NEW.Password = @hashedPassword;
END //

CREATE TRIGGER before_administrator_update
BEFORE UPDATE ON administrator
FOR EACH ROW
BEGIN
    CALL HashPassword(NEW.Password, @hashedPassword);
    SET NEW.Password = @hashedPassword;
END //

DELIMITER ;
