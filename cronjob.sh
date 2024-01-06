#!/bin/bash


output=$(git pull)
if [ "${output}" != "Already up to date." ]; then
  echo "here"
fi
