#!/bin/bash
cd /home/ubuntu/BOTC
output=$(git pull)
if [ "${output}" != "Already up to date." ]; then
  for pid in $(ps -ef | grep -v grep | grep botc-main.py | awk '{print $2}')
  do 
    echo "killing pid ${pid}" >> /tmp/botc-main.log 2>&1
    kill -9 ${pid}
  done
  sleep 5
  python3 botc-main.py >> /tmp/botc-main.log 2>&1 &
else
 pid=$(ps -ef | grep -v grep | grep botc-main.py | awk '{print $2}')
 if [ -z "${pid}" ]; then
   python3 botc-main.py >> /tmp/botc-main.log 2>&1 &
 fi
fi
