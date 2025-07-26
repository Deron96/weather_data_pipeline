🌦️ Weather Data Pipeline with GitHub Automation 🌦️ 

Overview: 
	
 This project pulls weather data from the OpenWeather API every 15 minutes, writes it to a PostgreSQL database, saves a daily CSV summary just after midnight, and auto-pushes everything to GitHub. It is 	running 24/7 on a GCP virtual machine I configured myself. I built this pipeline to sharpen my data engineering skills with real automation and version control.

Tech Stack:
	
  - Python (no external packages — just requests, json, csv, and psycopg2)
	- PostgreSQL for structured data storage
	- Google Cloud Platform (VM instance running 24/7)
	- Cron Jobs for scheduling scripts
	- Bash scripting for Git automation
	- Git & GitHub for version control and cloud syncing

How It Works:
  
  - Every 15 minutes:
  A cron job runs fetch_weather.py, hitting the OpenWeather API, flattening the JSON, and inserting a row into the PostgreSQL weather table.

  - At 12:05 AM:
  daily_records.py runs and queries all rows from the previous day, writing them to a dated CSV in the data/ folder.
	
  - At 12:15 AM:
  A bash script (auto_push.sh) stages all changes, commits them with a timestamp, and pushes the update to GitHub automatically. This includes the new daily CSV and logs.

File Structure:
```  
  weather_pipeline/
	  ├── data/                    # Stores raw JSON + daily CSVs
	  ├── logs/                    # Fetch and push logs
	  ├── fetch_weather.py         # Pulls data from API and inserts into Postgres
	  ├── daily_records.py         # Generates CSV from previous day's entries
	  ├── auto_push.sh             # Cron-executed GitHub push script
	  ├── .gitignore               # Keeps logs, backups, and secrets untracked
	  ├── requirements.txt         # Python package requirements
	  └── venv/                    # Virtual environment folder
```
Sample Output from them daily CSV:
```
  date		time	temp	feels_like	humidity	pressure	wind_speed
  2025-07-25	19:15	90.97	102.67		61		1016		4.61
  2025-07-25	19:30	90.97	102.67		61		1016		4.61
  2025-07-25	19:45	88.54	101.14		73		1016		2.46
  2025-07-25	20:00	87.57	100.17		75		1016		2.46
  2025-07-25	20:15	87.19	99.09		72		1017		3.44
```
Why This Project Matters:
	
  This pipeline runs unsupervised 24/7. It handles:

  - API interaction
  - Database ingestion
  - Time-based job scheduling
  - CSV export and data archiving
  - GitHub automation
  - Real-world ETL with zero manual work

Next Steps:
	
  - Add visualization/dashboard layer
	- Extend to multiple cities or metrics
