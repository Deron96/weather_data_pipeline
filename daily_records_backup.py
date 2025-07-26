import psycopg2
import csv
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

# Load environment variables (for PostgreSQL password)
load_dotenv()
PGPASSWORD = os.getenv("PGPASSWORD")

# Get today's date in EST
eastern = pytz.timezone("US/Eastern")
today = datetime.now(eastern).date()

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="weather",
    user="weather_user",
    password=PGPASSWORD,
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Query for today's records
cur.execute("""
    SELECT * FROM weather_data
    WHERE timestamp::date = %s
    ORDER BY timestamp ASC
""", (today,))

rows = cur.fetchall()
column_names = [desc[0] for desc in cur.description]

# Create dynamic filename based on today's date
output_path = os.path.expanduser(f"~/weather_pipeline/data/weather_{today}.csv")

# Write to CSV
with open(output_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(column_names)  # Write headers
    writer.writerows(rows)         # Write data rows

# Clean up
cur.close()
conn.close()
