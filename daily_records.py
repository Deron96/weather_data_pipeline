import psycopg2
import csv
from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv

# Load environment variables (for PostgreSQL password)
load_dotenv()
PGPASSWORD = os.getenv("PGPASSWORD")

# Get yesterday's date in EST
eastern = pytz.timezone("US/Eastern")
yesterday = datetime.now(eastern).date() - timedelta(days=1)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="weather",
    user="weather_user",
    password=PGPASSWORD,
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Query for yesterday's records
cur.execute("""
    SELECT * FROM weather_data
    WHERE timestamp::date = %s
    ORDER BY timestamp ASC
""", (yesterday,))

rows = cur.fetchall()
# Replace full timestamp with separate date and time (HH:MM)
simplified_rows = [
    (
        row[1].date().isoformat(),              # Date: '2025-07-25'
        row[1].strftime('%H:%M'),               # Time: '19:15'
        round(row[2], 2),                       # temp
        round(row[3], 2),                       # feels_like
        row[4],                                 # humidity
        row[5],                                 # pressure
        round(row[6], 2),                       # wind_speed
        row[7],                                 # weather_main
        row[8],                                 # weather_description
        row[9].strftime('%H:%M'),               # data_dt as time
        row[10].strftime('%H:%M'),              # sunrise as time
        row[11].strftime('%H:%M'),              # sunset as time
        row[12],                                # city
        row[13]                                 # unix_timestamp
    ) for row in rows
]

column_names = [
    'date', 'time', 'temp', 'feels_like', 'humidity', 'pressure', 'wind_speed',
    'weather_main', 'weather_description', 'data_time', 'sunrise', 'sunset',
    'city', 'unix_timestamp'
]

# Create dynamic filename based on yesterday's date
output_path = os.path.expanduser(f"~/weather_pipeline/data/weather_{yesterday}.csv")

# Write to CSV
with open(output_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(column_names)  # Write headers
    writer.writerows(simplified_rows)  # Write rows


# Clean up
cur.close()
conn.close()

print("HEAD:")
for row in simplified_rows[:3]:  
    print(row)

print("\nTAIL:")
for row in simplified_rows[-3:]: 
    print(row)

