#!/bin/bash

cd /home/dlester1996/weather_pipeline

# Activate the virtual environment (optional, safe to keep)
source venv/bin/activate

# Pull latest changes with auto-merge (avoids interactive prompt)
git pull --rebase --autostash origin main

# Add, commit, and push changes
git add .
git commit -m "Auto-push: $(date +'%Y-%m-%d %H:%M:%S')"
git push origin main
