#!/bin/bash
BASE=$1

if [[ $BASE = '' ]] ; then
  echo "usage: $0 BASE"
  exit 1
fi

# Try python3 if python is python2
if [[ `python --version 2>&1` = Python\ 2.7.* ]]
then PYTHON=python3
else PYTHON=python
fi

# Check GCloud parameter
PROJECT_ID=`jq .project_id "$GOOGLE_APPLICATION_CREDENTIALS" -r`
if [[ ! $PROJECT_ID ]]; then echo missing GOOGLE_APPLICATION_CREDENTIALS; exit; fi
echo GCloud: $PROJECT_ID

LOG=$BASE.out

# Launch the test
nohup $PYTHON $BASE.py > $LOG

# Copy log to storage
gsutil cp "$LOG" "gs://$PROJECT_ID/$BASE/`date -Iseconds`.log"

# Bye
sudo shutdown +2 # give a little time to cancel using: sudo shutdown -c
