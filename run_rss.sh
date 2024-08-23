#!/bin/bash

# Set the environment variable
export RSSVar=$HOME/ragno/rango-dev/bin/python3

# Change directory to where the config file is located
cd $HOME/ragno

# Runs the Python script using the Python interpreter specified ENV
$HOME/ragno/rango-dev/bin/python3 $HOME/ragno/scripts/send_rss_email.py

# Moves output
mv 2024-* ./output
