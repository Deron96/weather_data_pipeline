import requests
import psycopg2
from datetime import datetime
import pytz
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
PGPASSWORD = os.getenv("PGPASSWORD")

# Request weather data from OpenWeatherMap    
url = f"https://api.openweathermap.org/data/2.5/weather?q=Lynchburg,VA,US&appid={API_KEY}&units=imperial"
response = requests.get(url)
data = response.json()

# Extract and flatten the relevant fields
timestamp = datetime.now(pytz.timezone("US/Eastern"))
print(data)
temp = data["main"]["temp"]
feels_like = data["main"]["feels_like"]
humidity = data["main"]["humidity"]
pressure = data["main"]["pressure"]
wind_speed = data["wind"]["speed"]
weather_main = data["weather"][0]["main"]
weather_description = data["weather"][0]["description"]
unix_timestamp = data["dt"]

# Convert UNIX timestamps to readable datetime objects (EST)
eastern = pytz.timezone("US/Eastern")

data_dt = datetime.fromtimestamp(data["dt"], tz=pytz.utc).astimezone(eastern)
sunrise = datetime.fromtimestamp(data["sys"]["sunrise"], tz=pytz.utc).astimezone(eastern)
sunset = datetime.fromtimestamp(data["sys"]["sunset"], tz=pytz.utc).astimezone(eastern)


# Connect to PostgreSQL
conn = psycopg2.connect(
            dbname="weather",
	    user="weather_user",
	    password=PGPASSWORD,
	    host="localhost",
	    port="5432"
	    )
cur = conn.cursor()

# Insert data
cur.execute("""
    INSERT INTO weather_data (
        timestamp, temp, feels_like, humidity, pressure,
        wind_speed, weather_main, weather_description,
        data_dt, sunrise, sunset, city, unix_timestamp
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (
    timestamp, temp, feels_like, humidity, pressure,
    wind_speed, weather_main, weather_description,
    data_dt, sunrise, sunset, "Lynchburg", unix_timestamp
))


# Finalize and close
conn.commit()
cur.close()
conn.close()

# Save to JSON as a test
# Add converted EST timestamps to the JSON data for easy reference
data["timestamp_est"] = timestamp.isoformat()
data["data_dt_est"] = data_dt.isoformat()
data["sunrise_est"] = sunrise.isoformat()
data["sunset_est"] = sunset.isoformat()

with open(os.path.expanduser("~/weather_pipeline/data/raw_weather.json"), "w") as f:
    json.dump(data, f, indent=4)
