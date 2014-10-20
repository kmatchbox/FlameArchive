#!/bin/bash

# Gui interface for flamearchive.py

source=$(zenity --file-selection --directory --title="Select location of batch setups")

if [ "$?" == 1 ]
then
exit 0
fi

destination=$(zenity --file-selection --directory --title="Select location of archive")

if [ "$?" == 1 ]
then
exit 0
fi

filename=$(zenity --title="Enter name of archive (with .tar)" --entry)

if [ "$?" == 1 ]
then
exit 0
fi

python /usr/local/bin/flamearchive_gui.py $source ${destination}/${filename}

zenity --info --title="Flame Archive" --text="Archive complete."
