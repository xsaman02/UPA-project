from pymongo import MongoClient
import xml.etree.ElementTree as ET
import os


def create_station(elem, stationsDb):
    station = {"wmo-id": elem.get("wmo-id"),
               "bom-id": elem.get("bom-id"),
               "tz": elem.get("tz"),
               "stn-name": elem.get("stn-name"),
               "stn-height": elem.get("stn-height"),
               "type": elem.get("type"),
               "lat": elem.get("lat"),
               "lon": elem.get("lon"),
               "forecast-district-id": elem.get("forecast-district-id"),
               "description": elem.get("description"),
               "observations": []
               }
    stationsDb.insert_one(station)
    return stationsDb.find_one({"wmo-id": elem.get("wmo-id")})

def station(elem, stationsDb):
    currentStation = stationsDb.find_one({"wmo-id": elem.get("wmo-id")})

    if currentStation is None:
        currentStation = create_station(elem, stationsDb)

    observation = {}
    period = elem.find("period")
    observation["time-utc"] = period.get("time-utc")
    observation["time-local"] = period.get("time-local")
    observation["wind-src"] = period.get("wind-src")

    level = period.find("level")
    for element in level:
        observation[element.get("type")] = {"units": element.get("units"), "value": element.text}
        if element.get("start-time-local") is not None:
            observation[element.get("type")]["start-time-local"] = element.get("start-time-local")
        if element.get("end-time-local") is not None:
            observation[element.get("type")]["end-time-local"] = element.get("end-time-local")
        if element.get("end-time-utc") is not None:
            observation[element.get("type")]["end-time-utc"] = element.get("end-time-utc")
        if element.get("start-time-utc") is not None:
            observation[element.get("type")]["start-time-utc"] = element.get("start-time-utc")
        if element.get("instance") is not None:
            observation[element.get("type")]["instance"] = element.get("instance")
        if element.get("time-utc") is not None:
            observation[element.get("type")]["time-utc"] = element.get("time-utc")
        if element.get("time-local") is not None:
            observation[element.get("type")]["time-local"] = element.get("time-local")

    stationsDb.update_one({"wmo-id": elem.get("wmo-id")}, {"$push": {"observations": observation}})


client = MongoClient(port=27017)
client.drop_database("weather")  # TODO
print(client.list_database_names())

weatherDb = client["weather"]

stationsDb = weatherDb["stations"]

files = [os.path.join(dp, f) for dp, dn, filenames in os.walk("src/") for f in filenames if os.path.splitext(f)[1] == '.xml']

for file in files:
   tree = ET.parse(file)
   root = tree.getroot()

   observations = root.find('observations')

   for elem in observations:
      station(elem, stationsDb)


   print(stationsDb.count())


   for elem in stationsDb.find():
      print(elem)
