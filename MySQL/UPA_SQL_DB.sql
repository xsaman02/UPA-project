create database if not exists UPA_SQL_Db;
use UPA_SQL_Db;

-- ----------------- CHARSET -------------------------

ALTER DATABASE UPA_SQL_Db
    DEFAULT CHARACTER SET utf8mb4
	COLLATE utf8mb4_unicode_520_ci;


CREATE USER IF NOT EXISTS 'connector'@'localhost' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON UPA_SQL_Db . * TO 'connector'@'localhost';

-- ----------------- DROP TABLES ---------------------

DROP TABLE IF EXISTS SelectedWeatherReport;
DROP TABLE IF EXISTS Station;

-- ----------------- CREATE TABLES ---------------------

CREATE TABLE Station (WMO_ID INTEGER PRIMARY KEY NOT NULL,
                        Timezone VARCHAR(100),
                        Latitude FLOAT NOT NULL,
                        Longitude FLOAT NOT NULL,
                        TemperatureMedian FLOAT,
                        TemperatureNightMedian FLOAT,
                        TemperatureDayMedian FLOAT,
                        HumidityMedian DECIMAL(5,2),
                        RainfallMedian FLOAT
) ENGINE=InnoDB;

CREATE TABLE SelectedWeatherReport (AUTO_ID INTEGER AUTO_INCREMENT PRIMARY KEY NOT NULL,
                                    Station_ID INTEGER NOT NULL,
                                    Pressure FLOAT,
                                    Humidity DECIMAL(5,2),
                                    Rainfall FLOAT,
                                    CONSTRAINT FK_Station_ID FOREIGN KEY (Station_ID) REFERENCES Station(WMO_ID) 
                                        ON DELETE CASCADE
                                        ON UPDATE CASCADE
) ENGINE=InnoDB;


-- ----------------- TESTING DATA SETS ---------------------

-- INSERT INTO Station(WMO_ID, Timezone, Latitude, Longitude, TemperatureMedian, TemperatureNightMedian, TemperatureDayMedian, HumidityMedian, RainfallMedian)
--            VALUES (0, "Australia", 100.12, -56.378, 28.7, 22.5, 27.9, 37.6, 2);
-- INSERT INTO Station(WMO_ID, Timezone, Latitude, Longitude, TemperatureMedian, TemperatureNightMedian, TemperatureDayMedian, HumidityMedian, RainfallMedian)
--              VALUES (1, "Finland", 56098.1789, -523326.371318, 30.0, 23.8, 29.4, 25.6, 0.0);
-- INSERT INTO Station(WMO_ID, Timezone, Latitude, Longitude, TemperatureMedian, TemperatureNightMedian, TemperatureDayMedian, HumidityMedian, RainfallMedian)
--              VALUES (2, "Russia", -1265, -16131.3578, 25.3, 19.8, 24.2, 57, 12.7);
-- INSERT INTO Station(WMO_ID, Timezone, Latitude, Longitude, TemperatureMedian, TemperatureNightMedian, TemperatureDayMedian, HumidityMedian, RainfallMedian)
--              VALUES (3, "France", -0.1312, 12156.378, 34.5, 27.1, 33.9, 15.6, 0.2);

-- INSERT INTO SelectedWeatherReport(Station_ID, Pressure, Humidity, Rainfall)
--              VALUES (0, 1054.26, 37.78, 2.4);
-- INSERT INTO SelectedWeatherReport(Station_ID, Pressure, Humidity, Rainfall)
--              VALUES (0, 1154.26, 45.22, 12.1);
-- INSERT INTO SelectedWeatherReport(Station_ID, Pressure, Humidity, Rainfall)
--              VALUES (0, 1132.26, 42.34, 9.7);
-- INSERT INTO SelectedWeatherReport(Station_ID, Pressure, Humidity, Rainfall)
--              VALUES (2, 1000, 24.56, 0.4);
-- INSERT INTO SelectedWeatherReport(Station_ID, Pressure, Humidity, Rainfall)
--              VALUES (2, 1034.87, 22.55, 0.0);
-- INSERT INTO SelectedWeatherReport(Station_ID, Pressure, Humidity, Rainfall)
--              VALUES (3, 998.12, 15.67, 0.5);