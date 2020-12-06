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
	return mydb, mydb.cursor()

def calculate_median(weather_reports):
	""" Calculates median of all given weather reports

	Args:
	-----
		weather_reports (dict): weather report of given station

	Returns:
	--------
		[float, float, float]: median values of [temperature, humidity, rainfall]
	"""
	
	temp = []
	humidity = []
	rainfall = []
	for weather_report  in weather_reports:
		if "Maximum_temp" in weather_report and "Minimum_temp" in weather_report:
			temp.append(weather_report["Maximum_temp"] - weather_report["Minimum_temp"])
		if "Humidity" in weather_report:
			humidity.append(weather_report["Humidity"])
		if "Rainfall" in weather_report:
			rainfall.append(weather_report["Rainfall"])

	temp = sorted(temp)
	humidity = sorted(humidity)
	rainfall = sorted(rainfall)

	if len(temp) % 2 == 0:
		temp = (temp[len(temp)//2] + temp[len(temp)//2 - 1]) / 2
	else:
		temp = temp[len(temp)//2 - 1]
		

	if len(humidity) % 2 == 0:
		humidity = (humidity[len(humidity)//2] + humidity[len(humidity)//2 - 1]) / 2
	else:
		humidity = humidity[len(humidity)//2 - 1]


	if len(rainfall) % 2 == 0:
		rainfall = (rainfall[len(rainfall)//2] + rainfall[len(rainfall)//2 - 1]) / 2
	else:
		rainfall = rainfall[len(rainfall)//2 - 1]

	return {"temp_median" : temp, "humidity_median" : humidity, "rainfall_median" : rainfall}


def main():

	sql_db, sql_db_cursor  = connect_mySQL()
	mongo_db = connect_mongo()

	stations_mongo = mongo_db["stations"]

	#SQL INSERT TEST
	# sql_db_cursor.execute("""INSERT INTO Station(WMO_ID, Timezone, Latitude, Longitude, TemperatureMedian, TemperatureNightMedian, TemperatureDayMedian, HumidityMedian, RainfallMedian)
	#  VALUES (4, "Spain", 6876.32, -6876.32, 999.0, 100.0, 500.0, 0.0, 0.0);""")
	sql_db.commit()

	#SQL SELECT TEST
	sql_db_cursor.execute("SELECT * FROM Station;")
	print(sql_db_cursor.fetchall())


	stations = {}
	weather_reports = {}
	for station in stations_mongo.find():
		
		# if given station has not been seen before
		# store id of new station to the dictionary along with it's:
		# timezone, latitude, longitude
		if station["wmo-id"] not in stations:
			stations[station["wmo-id"]] = {"tz" : station["tz"], "lat" : station["lat"], "lon" : station["lon"]}
		
		for elements in station["observations"]:

			# if current station do not have any stored weather reports
			# store id of new station to dict with empty array (element in array is one report of given station)
			if station["wmo-id"] not in weather_reports:
				weather_reports[station["wmo-id"]] = []

			# Takes current data of given station
			station_data = weather_reports[station["wmo-id"]]
			data = {}

			# load addition data
			elements = station["observations"][0]
			data["FK"] = station["wmo-id"]
			if "rainfall_24hr" in elements:
				data["Rainfall"] = float(elements["rainfall_24hr"]["value"])
			if "pres" in elements:
				data["Pressure"] = float(elements["pres"]["value"])
			if "rel-humidity" in elements:
				data["Humidity"] = float(elements["rel-humidity"]["value"])
			if "maximum_air_temperature" in elements:
				data["Maximum_temp"] = float(elements["maximum_air_temperature"]["value"])
			if "minimum_air_temperature" in elements:
				data["Minimum_temp"] = float(elements["minimum_air_temperature"]["value"])
			# store data 
			station_data.append(data)



	#calculate medians and store them to station dictionary
	for station_key in stations.keys():
		medians = calculate_median(weather_reports[station_key])
		stations[station_key] = {**stations[station_key], **medians}


	# TODO
	# store every element in stations as Station in SQL
	# store every weather report in weather_reports as Weather-report in SQL
	# more info below
	"""
	Structure of station dictiory is array of dictionaries 
	where value of every dictionary is dictionary with wanted data. Via example:

	stations = [
		{wmo-id : {"tz" : timezone, 
				   "lat" : latitude, 
				   "lon" : longitude
				   "temp_median" : temperature median,
				   "humidity_median" : humidity median,
				   "rainfall_median" : rainfall median
				  }
		 ...
		},
	]

	Structure of weather_reports is array of dictionaries. Via example:

	weather_reports = 
	[
		{wmo-id : {"Rainfall" : value, 
				   "Pressure" : value, 
				   "Humidity" : value, 
				   "Maximum_temp" : value, 
				   "Minimum_temp" : value}
				  }
		 ...	
		},
	]
	""" 



		# sql_db.execute("""INSERT INTO Station(WMO_ID, Timezone, Latitude, Longitude, TemperatureMedian, TemperatureNightMedian, TemperatureDayMedian, HumidityMedian, RainfallMedian)
        #      VALUES (4, "Spain", -0.1312, 12156.378, 34.5, 27.1, 33.9, 15.6, 0.2);""")


if __name__ == "__main__":
	main()