from pymongo import MongoClient
import mysql.connector as cnt
import datetime
import os
import argparse


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
		if "time-local" in weather_report and type(weather_report["Air_temperature"]) != str:
			if day_start < weather_report["time-local"].time() < day_end:
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

	""" Parse imput arguments """
	parser = argparse.ArgumentParser(description="UPA - weather stations data analyzer")

	parser.add_argument('-r', action='store_true')

	args = parser.parse_args()

	# Run SELECT statements for initialized MySQL database
	if args.r:
		os.system("cd MySQL/ && make select")
		exit(0)
    	

	# Drop and setup new MySQL database
	os.system("cd MySQL/ && make drop")
	os.system("cd MySQL/ && make run")

	sql_db, sql_db_cursor  = connect_mySQL()
	mongo_db = connect_mongo()

	# Select colletion: stations
	stations_mongo = mongo_db["stations"]


	stations = {}
	weather_reports = {}
	for station in stations_mongo.find():
		
		# if given station has not been seen before
		# store id of new station to the dictionary along with it's:
		# timezone, latitude, longitude
		if station["wmo-id"] not in stations:
			stations[station["wmo-id"]] = {"tz" : station["tz"], "lat" : float(station["lat"]), "lon" : float(station["lon"]), "stn-name" : station["stn-name"]}
		
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

	print("Data fetched from MongoDb")

	#calculate medians and store them to station dictionary
	for station_key in stations.keys():
		medians = calculate_median(weather_reports[station_key])
		stations[station_key] = {**stations[station_key], **medians}

	print("Median calculations done")


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
		sql_db_cursor.execute("""INSERT INTO Station(WMO_ID, Latitude, Longitude, TemperatureMedian, TemperatureNightMedian, TemperatureDayMedian, HumidityMedian, RainfallMean, StationName)
			VALUES ('%d', '%f', '%f', %s, %s, %s, %s, %s, '%s');"""
			% (int(ID), stations[ID]['lat'], stations[ID]['lon'], stations[ID]['temp_median'], stations[ID]["night_temp_median"], stations[ID]["day_temp_median"], stations[ID]['humidity_median'], stations[ID]['rainfall_mean'], stations[ID]['stn-name']))
		sql_db.commit()
	print("Stations successfully inserted into MySQL database")

	for ID in weather_reports:
		for report in weather_reports[ID]:
			sql_db_cursor.execute("""INSERT INTO SelectedWeatherReport(Station_ID, Pressure, Humidity, Rainfall)
				VALUES ('%d', %s, %s, %s);"""
				% (int(ID), report['Pressure'], report['Humidity'], report['Rainfall']))
		sql_db.commit()	
		
	print("Weather reports successfully inserted into MySQL database")



if __name__ == "__main__":
	main()