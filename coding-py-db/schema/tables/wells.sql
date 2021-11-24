CREATE TABLE `global`.`wells` (
    `well_name` VARCHAR(128) NOT NULL,
    `id` VARCHAR(12) NOT NULL,
    `perf_lateral_length` INT NULL,
    `api_14` VARCHAR(14) NOT NULL,
    `county` VARCHAR(64) NULL,
    `state` VARCHAR(64) NOT NULL,
    PRIMARY KEY (`well_name`, `id`),
    UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
    UNIQUE INDEX `api_14_UNIQUE` (`api_14` ASC) VISIBLE
);
