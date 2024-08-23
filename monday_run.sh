#!/bin/bash
# This script is used to start the monday_special python script
# monday_special pulls news over the last 70 hours

# Set the environment variable
export RSSVar=$HOME/ragno/rango-dev/bin/python3

# Change directory to where the config file is located
cd $HOME/ragno

# Runs the Python script using the Python interpreter specified ENV
$HOME/ragno/rango-dev/bin/python3 $HOME/ragno/scripts/monday_special.py

# Moves output
mv 2024-* ./output
