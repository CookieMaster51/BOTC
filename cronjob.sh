#!/bin/bash

output=$(git pull)
if [ "${output}" != "Already up to date." ]; then
  pid=$(ps -ef | grep -v grep | grep botc-main.py | awk '{print $2}')
  if [ -n "${pid}" ]; then
    kill -9 ${pid}
    sleep 5
  fi
  python3 botc-main.py &
else
 pid=$(ps -ef | grep -v grep | grep botc-main.py | awk '{print $2}')
 if [ -z "${pid}" ]; then
   python3 botc-main.py &
 fi
fi


