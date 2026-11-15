import requests
import datetime as dt
import pandas as pd
from zoneinfo import ZoneInfo
import time

people_dataframe = pd.read_csv("people.csv")
people_to_notify = people_dataframe.to_dict(orient="records")


def geocode_person(person):
    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search", params={"name": person["city"], "count": 1}
    )
    response.raise_for_status()
    data = response.json()
    person["latitude"] = data["results"][0]["latitude"]
    person["longitude"] = data["results"][0]["longitude"]
    person["timezone"] = data["results"][0]["timezone"]


def update_sun_times(person):
    sun_parameters = {
        "lat": person["latitude"],
        "lng": person["longitude"],
    }
    response = requests.get("https://api.sunrise-sunset.org/v2", params=sun_parameters)
    response.raise_for_status()
    data = response.json()
    person["dawn"] = dt.datetime.fromisoformat(data["dawn"])
    person["dusk"] = dt.datetime.fromisoformat(data["dusk"])


def is_dark(person, timenow):
    return not (person["dawn"] <= timenow <= person["dusk"])


def get_iss_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    return iss_latitude, iss_longitude


def is_iss_above(person, iss_lat, iss_long):
    lat_close = abs(iss_lat - person["latitude"]) <= 5
    long_close = abs(iss_long - person["longitude"]) <= 5
    return lat_close and long_close


for person in people_to_notify:
    geocode_person(person)
    update_sun_times(person)


while True:
    iss_lat, iss_long = get_iss_position()
    print("Iss:", iss_lat, iss_long)
    for person in people_to_notify:
        now = dt.datetime.now(ZoneInfo(person["timezone"]))
        if now.date() != person["dawn"].date():
            update_sun_times(person)
        print(person["name"], ":", person["latitude"], person["longitude"])
        if is_dark(person, now) and is_iss_above(person, iss_lat, iss_long):
            print("Look up")

    time.sleep(10)
