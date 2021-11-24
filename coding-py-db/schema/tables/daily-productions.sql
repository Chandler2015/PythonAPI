CREATE TABLE `global`.`daily_productions` (
    `oil` INT NULL,
    `gas` INT NULL,
    `water` INT NULL,
    `id` INT GENERATED ALWAYS AS (),
    `well` VARCHAR(12) NOT NULL,
    `date` DATETIME NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
    INDEX `well_idx` (`well` ASC) VISIBLE,
    CONSTRAINT `well` FOREIGN KEY (`well`) REFERENCES `global`.`wells` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
);
