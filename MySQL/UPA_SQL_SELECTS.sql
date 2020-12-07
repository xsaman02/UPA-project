create database if not exists UPA_SQL_Db;
use UPA_SQL_Db;


-- ----------------- SELECT A: ALL DATA ---------------------

-- SELECT "" AS "--------------------------- SELECT A: Temperature START ----------------------------";
-- SELECT Station.WMO_ID, Station.StationName, Station.Latitude, Station.Longitude, Station.TemperatureMedian FROM Station
-- WHERE TemperatureMedian != "NULL"
-- ORDER BY TemperatureMedian DESC;
-- SELECT "" AS "--------------------------- SELECT A: Temperature END ----------------------------";
-- SELECT "" AS "--------------------------- SELECT A: Rainfall START ----------------------------";
-- SELECT Station.WMO_ID, Station.StationName, Station.Latitude, Station.Longitude, Station.RainfallMean FROM Station
-- WHERE RainfallMean != "NULL"
-- ORDER BY RainfallMean;
-- SELECT "" AS "--------------------------- SELECT A: Rainfall END ----------------------------";


-- ----------------- SELECT A: SELECTED DATA ---------------------

-- ----------------- SELECT A: TOP 20 ---------------------
SELECT "" AS "--------------------------- SELECT A: Top 20 Temperature START ----------------------------";
SELECT Station.WMO_ID, Station.StationName, Station.Latitude, Station.Longitude, Station.TemperatureMedian FROM Station
WHERE TemperatureMedian != "NULL"
ORDER BY TemperatureMedian DESC
LIMIT 20;
SELECT "" AS "--------------------------- SELECT A: Top 20 Temperature END ----------------------------";
SELECT "" AS " ";
SELECT "" AS "--------------------------- SELECT A: Top 20 Rainfall START ----------------------------";
SELECT Station.WMO_ID, Station.StationName, Station.Latitude, Station.Longitude, Station.RainfallMean FROM Station
WHERE RainfallMean != "NULL"
ORDER BY RainfallMean DESC
LIMIT 20;
SELECT "" AS "--------------------------- SELECT A: Top 20 Rainfall END ----------------------------";
SELECT "" AS " ";

-- ----------------- SELECT A: LAST 20 ---------------------
SELECT "" AS "--------------------------- SELECT A: Last 20 Temperature START ----------------------------";
SELECT Station.WMO_ID, Station.StationName, Station.Latitude, Station.Longitude, Station.TemperatureMedian FROM Station
WHERE TemperatureMedian != "NULL"
ORDER BY TemperatureMedian ASC
LIMIT 20;
SELECT "" AS "--------------------------- SELECT A: Last 20 Temperature END ----------------------------";
SELECT "" AS " ";
SELECT "" AS "--------------------------- SELECT A: Last 20 Rainfall START ----------------------------";
SELECT Station.WMO_ID, Station.StationName, Station.Latitude, Station.Longitude, Station.RainfallMean FROM Station
WHERE RainfallMean != "NULL"
ORDER BY RainfallMean ASC
LIMIT 20;
SELECT "" AS "--------------------------- SELECT A: Last 20 Rainfall END ----------------------------";
SELECT "" AS " ";


-- ----------------- SELECT B: ---------------------

SELECT "" AS "--------------------------- SELECT B: START ----------------------------";
SELECT Station.Latitude, Station.TemperatureDayMedian, Station.TemperatureNightMedian FROM Station
WHERE Station.TemperatureDayMedian != "NULL" AND Station.TemperatureNightMedian != "NULL"
ORDER BY Station.Latitude;
SELECT "" AS "--------------------------- SELECT B: END ----------------------------";
SELECT "" AS " ";

-- ----------------- SELECT C: ---------------------

SELECT "" AS "--------------------------- SELECT C: START ----------------------------";
SELECT Station.WMO_ID, SelectedWeatherReport.Pressure, SelectedWeatherReport.Humidity, SelectedWeatherReport.Rainfall FROM Station
INNER JOIN SelectedWeatherReport ON Station.WMO_ID = SelectedWeatherReport.Station_ID
WHERE Rainfall != "NULL" AND Humidity != "NULL" AND Pressure != "NULL"
ORDER BY Pressure;
SELECT "" AS "--------------------------- SELECT C: END ----------------------------";