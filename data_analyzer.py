from pymongo import MongoClient
import mysql.connector as cnt
import datetime

def connect_mongo():
	client = MongoClient(port=27017)
	mongo_db = client["weather"]
	return mongo_db

def connect_mySQL():
	mydb = cnt.connect(
	host="localhost",
	user="connector",
	passwd="123456",
	database="UPA_SQL_Db")
	return mydb

def calculate_median(row):
	...



def main():

	sql_db = connect_mySQL()
	sql_db_cursor = sql_db.cursor()
	mongo_db = connect_mongo()

	stations = mongo_db["station"]
	temp_night = []
	temp_day = []
	temp = []
	rainfall_24 = []

	sql_station = {}
	sql_selected_weather_report = {}

	#SQL INSERT TEST
	sql_db_cursor.execute("""INSERT INTO Station(WMO_ID, Timezone, Latitude, Longitude, TemperatureMedian, TemperatureNightMedian, TemperatureDayMedian, HumidityMedian, RainfallMedian)
	 VALUES (4, "Spain", 6876.32, -6876.32, 999.0, 100.0, 500.0, 0.0, 0.0);""")
	sql_db.commit()

	#SQL SELECT TEST
	sql_db_cursor.execute("SELECT * FROM Station;")
	print(sql_db_cursor.fetchall())

	for station in stations.find():
		
		elements = station["observations"][0]

		# TODO výpočet mediánů
		# temp_night.append(elements["air_temperature"]["value"])
		# temp_day.append(elements["air_temperature"]["value"])
		# temp.append(elements["air_temperature"]["value"])
		# rainfall_24.append(elements["rainfall_24hr"]["value"])
		
		sql_station["Timezone"] = station["tz"]
		sql_station["Latitude"] = station["lat"]
		sql_station["Longitude"] = station["lon"]
		sql_station["TemperatureDayMedian"] = None
		sql_station["TemperatureNightMedian"] = None
		sql_station["TemperatureMedian"] = None
		sql_station["HumidityMedian"] = None
		sql_station["RainfallMedian"] = None
		

		sql_selected_weather_report["FK"] = station["wmo-id"]
		sql_selected_weather_report["Rainfall"] = elements["rainfall_24hr"]["value"]
		sql_selected_weather_report["Pressure"] = elements["pres"]["value"]
		sql_selected_weather_report["Humidity"] = elements["rel-humidity"]["value"]

		sql_db.execute("""INSERT INTO Station(WMO_ID, Timezone, Latitude, Longitude, TemperatureMedian, TemperatureNightMedian, TemperatureDayMedian, HumidityMedian, RainfallMedian)
             VALUES (4, "Spain", -0.1312, 12156.378, 34.5, 27.1, 33.9, 15.6, 0.2);""")


if __name__ == "__main__":
	main()