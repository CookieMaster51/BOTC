#!/bin/bash


output=$(git pull)
if [ "${output}" != "Already up to date." ]; then
  pid=$(ps -ef | grep botc-main.py | awk '{print $1}')
fi


