#!/bin/bash

cd /home/dlester1996/weather_pipeline

# Activate the virtual environment (optional, if needed for git config or Python prep)
source venv/bin/activate

# Pull latest changes FIRST
git pull origin main

# Add, commit, and push changes
git add .
git commit -m "Auto-push: $(date +'%Y-%m-%d %H:%M:%S')"
git push origin main
