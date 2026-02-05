#!/bin/bash
cd /home/pi/art-display
source .venv/bin/activate
exec watchmedo auto-restart --patterns="*.py;*.json" --recursive -- python backend/app.py
