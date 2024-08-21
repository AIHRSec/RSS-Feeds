#!/bin/bash

# Variable of pervious year and month plus wildcard
previous_month=$(date --date='-1 month' '+%Y-%m')-*

# For testing only
ls $HOME/ragno/output/$previous_month > $HOME/ragno/logs/Previous_Months_Files.txt

# Deletes all the files that follow the variable format YYYY-MM-*
rm $HOME/ragno/output/$previous_month
