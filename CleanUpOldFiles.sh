#!/bin/bash

# Variable of previous year and month plus wildcard
previous_month=$(date --date='-1 month' '+%Y-%m')-*

# For testing only
ls ~/output/$previous_month > ~/logs/Previous_Month_Files.txt

# Deletes all the files that follow the variable format YYYY-MM-*
rm ~/output/$previous_month
