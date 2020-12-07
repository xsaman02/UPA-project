create database if not exists UPA_SQL_Db;
use UPA_SQL_Db;

-- ----------------- SELECTS ---------------------

-- SELECT Station.* FROM Station;
-- SELECT "" as " ";

-- SELECT SelectedWeatherReport.* FROM SelectedWeatherReport;
-- SELECT "" as " ";

-- ----------------- SELECT A: ---------------------

SELECT "" AS "--------------------------- SELECT A: Temperature START ----------------------------";
SELECT Station.WMO_ID, Station.Timezone, Station.Latitude, Station.Longitude, Station.TemperatureMedian FROM Station
WHERE TemperatureMedian != "NULL"
ORDER BY TemperatureMedian DESC;
SELECT "" AS "--------------------------- SELECT A: Temperature END ----------------------------";
SELECT "" AS "--------------------------- SELECT A: Rainfall START ----------------------------";
SELECT Station.WMO_ID, Station.Timezone, Station.Latitude, Station.Longitude, Station.RainfallMedian FROM Station
WHERE RainfallMedian != "NULL"
ORDER BY RainfallMedian DESC;
SELECT "" AS "--------------------------- SELECT A: Rainfall END ----------------------------";


-- ----------------- SELECT C: ---------------------

SELECT "" AS "--------------------------- SELECT C: START ----------------------------";
SELECT Station.WMO_ID, SelectedWeatherReport.Pressure, SelectedWeatherReport.Humidity, SelectedWeatherReport.Rainfall FROM Station
INNER JOIN SelectedWeatherReport ON Station.WMO_ID = SelectedWeatherReport.Station_ID;
SELECT "" AS "--------------------------- SELECT C: END ----------------------------";