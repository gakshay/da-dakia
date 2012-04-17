#!/bin/bash

# Check the credentials here first before running the script
PROJECTDIR=$PWD
LOCALEXPORTDIR=$LOCALEXPORTDIR/files/send
OUTBOX=$LOCALEXPORTDIR/outbox
INBOX=$LOCALEXPORTDIR/inbox
LOGDIR=$LOCALEXPORTDIR/log
PROCDIR=$LOCALEXPORTDIR/processing
CONTROLDIR=$LOCALEXPORTDIR/control
ERRORDIR=$LOCALEXPORTDIR/error
ARCHIVEDIR=$LOCALEXPORTDIR/archive
mkdir -p $INBOX $OUTBOX $LOGDIR $PROCDIR $CONTROLDIR $ERRORDIR $ARCHIVEDIR


# ========================================================
# PROGRAM start
# ========================================================

# ========================================================
# Helper functions to maintain log entries in the project
# ========================================================
check_error() {
    if [ "$1" -ne "0" ]; then
        echo "Export $3:`date +\"%d-%m-%y:%T\"`: $2"
    return 1
    fi  
  return 0
}

log_entry(){
  echo "Export $2:`date +"%d-%m-%y:%T"` :$1" 
}

file_exists(){
  for file in $1/*.txt
  do  
    if [ -f "$file" ]; then
      return 0
    fi  
    return 1
  done
}

dir_exists(){
  if [ "$(ls -A $1)" ]; then
    return 0
  else
    return 1
  fi
}

# ========================================================
# Check if internet is working                            
# ========================================================
sh ${PROJECTDIR}/scripts/internet.sh                      
if [ $? -eq 1 ]; then                                     
  log_entry "No internet access" "ERROR"                  
  exit 0                                                  
fi  

# ========================================================
# 1. moving inbox files to outbox
# ========================================================
dir_exists $INBOX
check_error $? "Nothing to move to outbox from inbox" "NOTICE"
ret_val=$?
if [ "$ret_val" -ne "1" ]; then
  log_entry "moving files to outbox for processing" INFO
  cp -r $INBOX/* $OUTBOX/
  rm -r $INBOX/*
fi


# ========================================================
# 2 export files to eDakia Cloud if any
# ========================================================
dir_exists $OUTBOX
check_error $? "Nothing to export to eDakia Cloud" "NOTICE"
ret_val=$?
if [ "$ret_val" -ne "1" ]; then
  log_entry "Files Export to eDakia server" INFO
  sh $PROJECTDIR/scripts/transfer_send.sh
  check_error $? "Files export to eDakia Cloud failed" "ERROR"
fi
