CREATE SCHEMA IF NOT EXISTS `pharmacy` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `pharmacy` ;

-- -----------------------------------------------------
-- Table `pharmacy`.`assignationmedicament`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pharmacy`.`assignationmedicament` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Groupmedicament` VARCHAR(255) NULL DEFAULT NULL,
  `Description` TEXT NULL DEFAULT NULL,
  `Image` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pharmacy`.`client`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pharmacy`.`client` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(255) NULL DEFAULT NULL,
  `Login` VARCHAR(255) NULL DEFAULT NULL,
  `Password` VARCHAR(255) NULL DEFAULT NULL,
  `Representative` VARCHAR(255) NULL DEFAULT NULL,
  `Adress` TEXT NULL DEFAULT NULL,
  `Phonenumber` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pharmacy`.`diseases`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pharmacy`.`diseases` (
  `Illness` VARCHAR(255) NULL DEFAULT NULL,
  `IDAssignationmedicament` INT NULL DEFAULT NULL,
  INDEX `IDAssignationmedicament` (`IDAssignationmedicament` ASC) VISIBLE,
  CONSTRAINT `diseases_ibfk_1`
    FOREIGN KEY (`IDAssignationmedicament`)
    REFERENCES `pharmacy`.`assignationmedicament` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pharmacy`.`employee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pharmacy`.`employee` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Fullname` VARCHAR(255) NULL DEFAULT NULL,
  `Post` VARCHAR(255) NULL DEFAULT NULL,
  `Login` VARCHAR(255) NULL DEFAULT NULL,
  `Password` VARCHAR(255) NULL DEFAULT NULL,
  `Birthdate` DATE NULL DEFAULT NULL,
  `Dateofhiring` DATE NULL DEFAULT NULL,
  `Phonenumber` VARCHAR(255) NULL DEFAULT NULL,
  `Photo` VARCHAR(255) NULL DEFAULT NULL,
  `Education` VARCHAR(255) NULL DEFAULT NULL,
  `Salary` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pharmacy`.`provider`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pharmacy`.`provider` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(255) NULL DEFAULT NULL,
  `Representative` VARCHAR(255) NULL DEFAULT NULL,
  `Post` VARCHAR(255) NULL DEFAULT NULL,
  `Phonenumber` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pharmacy`.`medicament`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pharmacy`.`medicament` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(255) NULL DEFAULT NULL,
  `IDAssignationmedicament` INT NULL DEFAULT NULL,
  `IDProvider` INT NULL DEFAULT NULL,
  `Unitsofmeasurement` VARCHAR(255) NULL DEFAULT NULL,
  `Pricepurchase` DECIMAL(10,2) NULL DEFAULT NULL,
  `Pricerealization` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `IDAssignationmedicament` (`IDAssignationmedicament` ASC) VISIBLE,
  INDEX `IDProvider` (`IDProvider` ASC) VISIBLE,
  CONSTRAINT `medicament_ibfk_1`
    FOREIGN KEY (`IDAssignationmedicament`)
    REFERENCES `pharmacy`.`assignationmedicament` (`id`),
  CONSTRAINT `medicament_ibfk_2`
    FOREIGN KEY (`IDProvider`)
    REFERENCES `pharmacy`.`provider` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pharmacy`.`orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pharmacy`.`orders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `IDClient` INT NULL DEFAULT NULL,
  `IDEmployee` INT NULL DEFAULT NULL,
  `Dateofplacement` DATE NULL DEFAULT NULL,
  `Dateappointment` DATE NULL DEFAULT NULL,
  `Dateperformance` DATE NULL DEFAULT NULL,
  `Deliverycost` DECIMAL(10,2) NULL DEFAULT NULL,
  `Recipient` VARCHAR(255) NULL DEFAULT NULL,
  `Recipientaddress` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `IDClient` (`IDClient` ASC) VISIBLE,
  INDEX `IDEmployee` (`IDEmployee` ASC) VISIBLE,
  CONSTRAINT `orders_ibfk_1`
    FOREIGN KEY (`IDClient`)
    REFERENCES `pharmacy`.`client` (`id`),
  CONSTRAINT `orders_ibfk_2`
    FOREIGN KEY (`IDEmployee`)
    REFERENCES `pharmacy`.`employee` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `pharmacy`.`ordered`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pharmacy`.`ordered` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `IDMedicament` INT NULL DEFAULT NULL,
  `Pricerealization` DECIMAL(10,2) NULL DEFAULT NULL,
  `Quantity` INT NULL DEFAULT NULL,
  `orders_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `IDMedicament` (`IDMedicament` ASC) VISIBLE,
  INDEX `fk_ordered_orders1_idx` (`orders_id` ASC) VISIBLE,
  CONSTRAINT `ordered_ibfk_1`
    FOREIGN KEY (`IDMedicament`)
    REFERENCES `pharmacy`.`medicament` (`id`),
  CONSTRAINT `fk_ordered_orders1`
    FOREIGN KEY (`orders_id`)
    REFERENCES `pharmacy`.`orders` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;
