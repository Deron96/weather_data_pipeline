#!/bin/bash

cd /home/dlester1996/weather_pipeline
source venv/bin/activate

# Pull latest changes (auto-resolve with rebase)
git pull --rebase origin main

# Add, commit, and push changes
git add .
git commit -m "Auto-push: $(date +'%Y-%m-%d %H:%M:%S')"
git push origin main
