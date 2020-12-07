from pymongo import MongoClient
import mysql.connector as cnt
import datetime
import os


#GLOBAL COMPATIBILITY VARIABLE:
NULL = "NULL"


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
		[float, float, float, float, float]: median values of [temperature, humidity, rainfall, day_temp_median, night_temp_median]
	"""
	day_start = datetime.time(10, 0, 0, 0)
	day_end = datetime.time(22, 0, 0, 0)
	
	temp = []
	humidity = []
	rainfall = []
	day_temp = []
	night_temp = []
	for weather_report  in weather_reports:
		if "Air_temperature" in weather_report and type(weather_report["Air_temperature"]) != str:
			temp.append(weather_report["Air_temperature"])
		if "Humidity" in weather_report and type(weather_report["Humidity"]) != str:
			humidity.append(weather_report["Humidity"])
		if "Rainfall" in weather_report and type(weather_report["Rainfall"]) != str:
			rainfall.append(weather_report["Rainfall"])
		if "time-local" in weather_report:
			if day_start < weather_report["time_local"].time() < day_end:
				day_temp.append(weather_report["Air_temperature"])
			else:
				night_temp.append(weather_report["Air_temperature"])

	temp = sorted(temp)
	humidity = sorted(humidity)
	rainfall = sorted(rainfall)

	if(len(temp) == 0):
		temp=NULL
	else:
		if len(temp) % 2 == 0:
			temp = (temp[len(temp)//2] + temp[len(temp)//2 - 1]) / 2
		else:
			temp = temp[len(temp)//2 - 1]
		
	if(len(humidity) == 0):
		humidity=NULL
	else:
		if len(humidity) % 2 == 0:
			humidity = (humidity[len(humidity)//2] + humidity[len(humidity)//2 - 1]) / 2
		else:
			humidity = humidity[len(humidity)//2 - 1]

	if(len(day_temp) == 0):
		day_temp = NULL
	else:
		if len(day_temp) % 2 == 0:
			day_temp = (day_temp[len(day_temp)//2] + day_temp[len(day_temp)//2 - 1]) / 2
		else:
			day_temp = day_temp[len(day_temp)//2 - 1]

	if(len(night_temp) == 0):
		night_temp = NULL
	else:
		if len(night_temp) % 2 == 0:
			night_temp = (night_temp[len(night_temp)//2] + night_temp[len(night_temp)//2 - 1]) / 2
		else:
			night_temp = night_temp[len(night_temp)//2 - 1]

	if(len(rainfall) == 0):
		rainfall=NULL
	else:
		rainfall = sum(rainfall) / len(rainfall)

	return {"temp_median" : temp, "humidity_median" : humidity, "rainfall_mean" : rainfall, "day_temp_median" : day_temp, "night_temp_median" : night_temp}


def main():

	os.system("cd MySQL/ && make drop << pwd")
	os.system("cd MySQL/ && make run << pwd")

	sql_db, sql_db_cursor  = connect_mySQL()
	mongo_db = connect_mongo()

	# Select colletion: stations
	stations_mongo = mongo_db["stations"]

	#SQL INSERT TEST
	# sql_db_cursor.execute("""INSERT INTO Station(WMO_ID, Timezone, Latitude, Longitude, TemperatureMedian, TemperatureNightMedian, TemperatureDayMedian, HumidityMedian, RainfallMedian)
	#  VALUES (4, "Spain", 6876.32, -6876.32, NULL, 100.0, NULL, 0.0, 0.0);""")
	# sql_db.commit()

	#SQL SELECT TEST
	# sql_db_cursor.execute("SELECT * FROM Station;")
	# print(sql_db_cursor.fetchall())


	stations = {}
	weather_reports = {}
	for station in stations_mongo.find():
		
		# if given station has not been seen before
		# store id of new station to the dictionary along with it's:
		# timezone, latitude, longitude
		if station["wmo-id"] not in stations:
			stations[station["wmo-id"]] = {"tz" : station["tz"], "lat" : float(station["lat"]), "lon" : float(station["lon"])}
		
		for elements in station["observations"]:

			# if current station do not have any stored weather reports
			# store id of new station to dict with empty array (element in array is one report of given station)
			if station["wmo-id"] not in weather_reports:
				weather_reports[station["wmo-id"]] = []

			# Takes current data of given station
			station_data = weather_reports[station["wmo-id"]]
			data = {}

			# load addition data
			data["FK"] = station["wmo-id"]
			if "rainfall" in elements:
				data["Rainfall"] = float(elements["rainfall"]["value"])
			else:
				data["Rainfall"] = NULL
			
			if "pres" in elements:
				data["Pressure"] = float(elements["pres"]["value"])
			else:
				data["Pressure"] = NULL
			
			if "rel-humidity" in elements:
				data["Humidity"] = float(elements["rel-humidity"]["value"])
			else:
				data["Humidity"] = NULL
			
			if "air_temperature" in elements:					
				data["Air_temperature"] = float(elements["air_temperature"]["value"])
			else:
				data["Air_temperature"] = NULL

			if "time-local" in elements:
				data["time-local"] = datetime.datetime.strptime(elements["time-local"].split('+')[0], '%Y-%m-%dT%H:%M:%S')
			# store data 
			station_data.append(data)

	print("Data fetched")

	#calculate medians and store them to station dictionary
	for station_key in stations.keys():
		medians = calculate_median(weather_reports[station_key])
		stations[station_key] = {**stations[station_key], **medians}

	print("Medians done")

	# TODO
	# store every element in stations as Station in SQL
	# store every weather report in weather_reports as Weather-report in SQL
	# more info below
	"""
	Structure of station dictiory is array of dictionaries 
	where value of every dictionary is dictionary with wanted data. Via example:

	stations = {
		wmo-id : {"tz" : value, 
				   "lat" : value, 
				   "lon" : value,
				   "temp_median" : value,
				   "humidity_median" : value,
				   "rainfall_median" : value,
				   "day_temp_median" : value,
				   "night_temp_median" : value
				  },
		 ...
		,
	}

	Structure of weather_reports is array of dictionaries. Via example:

	weather_reports = 
	{
		wmo-id : [{
				   "Rainfall" : value, 
				   "Pressure" : value, 
				   "Humidity" : value, 
				   "Maximum_temp" : value, 
				   "Minimum_temp" : value}
				  },
				  ...
				 ]
		 ...	
		,
	}
	""" 


	""" Insert selected station data from MongoDb to MySQL database """
	for ID in stations:
		sql_db_cursor.execute("""INSERT INTO Station(WMO_ID, Timezone, Latitude, Longitude, TemperatureMedian, TemperatureNightMedian, TemperatureDayMedian, HumidityMedian, RainfallMedian)
			VALUES ('%d', '%s', '%f', '%f', %s, %s, %s, %s, %s);"""
<<<<<<< HEAD
			% (int(ID), stations[ID]['tz'], stations[ID]['lat'], stations[ID]['lon'], stations[ID]['temp_median'], stations[ID]["temp_night_median"], stations[ID]["temp_day_median"], stations[ID]['humidity_median'], stations[ID]['rainfall_mean']))
		sql_db.commit()
=======
			% (int(ID), stations[ID]['tz'], stations[ID]['lat'], stations[ID]['lon'], stations[ID]['temp_median'], NULL, NULL, stations[ID]['humidity_median'], stations[ID]['rainfall_median']))
	sql_db.commit()	

	print("Station insert done")
>>>>>>> b10876e0b98ef6e8d42c3be75a7d60d8ec955344

	for i, ID in enumerate(weather_reports):
		print(i+1)
		for report in weather_reports[ID]:
			sql_db_cursor.execute("""INSERT INTO SelectedWeatherReport(Station_ID, Pressure, Humidity, Rainfall)
				VALUES ('%d', %s, %s, %s);"""
				% (int(ID), report['Pressure'], report['Humidity'], report['Rainfall']))
		sql_db.commit()	
		
	print("Weather insert done")

	# sql_db_cursor.execute("SELECT * FROM Station;")	
	# for row in sql_db_cursor.fetchall():
	# 	print(row)


if __name__ == "__main__":
	main()