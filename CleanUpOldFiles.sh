#!/bin/bash

# Variable of previous year and month plus wildcard
previous_month=$(date --date='-1 month' '+%Y-%m')

# Deletes all the files that follow the variable format YYYY-MM-*
#rm $month

# For testing only
ls $month > test.txt
