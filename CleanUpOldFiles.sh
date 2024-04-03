#!/bin/bash

# Variable of current year and month plus wildcard 
month=$(date '+%Y-%m')-*

# Deletes all the files that follow the variable format YYYY-MM-*
#rm $month

# For testing only
ls $month > ~/test.txt