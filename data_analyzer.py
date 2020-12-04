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
	user="root",
	passwd="rfDOBAD",
	database="xstoja07",
	)
	return mydb

def calculate_median(row):
	...


def main():
	mongo_db = connect_mongo()
	sql_db = connect_mySQL()

	stations = mongo_db["station"].find()
	temp_night = []
	temp_day = []
	temp = []
	rainfall_24 = []

	sql_station = {}
	sql_selected_weather_report = {}

	for station in stations:
		
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




if __name__ == "__main__":
	main()