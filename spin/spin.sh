#!/bin/bash
# Print a spinning line

speed=$1
arr=("|" "/" "-" "\\" "|" "/" "-" "\\")

while :
do
  for i in "${arr[@]}"
  do
    echo -n "$i"
    sleep $speed
    echo -ne '\r'
  done
done
