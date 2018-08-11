#!/bin/bash

TMP_DIR="/tmp/"
DATE=$(date +"%d-%m-%Y_%H%M")
BKP_FILE="masterdata.csv"
BKP_DIRS="/home/pi/Robo_Reef/"
DROPBOX_UPLOADER=/home/pi/Robo_Reef/Dropbox-Uploader-master/dropbox_uploader.sh


$DROPBOX_UPLOADER -f .dropbox_uploader upload "$BKP_DIRS" /
