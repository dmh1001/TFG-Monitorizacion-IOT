#!/bin/bash

IFS=$'\n'
for LINE in $(cat $1)
do
   echo $LINE
   curl -XPOST -u sensor_data:sensor_data --header "Content-Type: application/json" "http://localhost:8080/" -d ''$LINE''
done
