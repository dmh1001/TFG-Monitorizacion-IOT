#!/bin/bash

sensorId="1006"
startDate="16/04/2021"
startTime="19:00:00"

endDate="16/04/2021"
endTime="19:50:00"


elasticdump \
  --input=http://localhost:9200/sensor_data-* \
  --output=/home/elk/data'$startDate'.json\
  --type=data \
  --searchBody='{"query": {"bool": {"must": [{ "match": { "sensorId":"'$sensorId'" } },{ "range": {"datetime" : { "gt" : "'$startDate' '$startTime'","lte" : "'$endDate' '$endTime'"}}}]}}}'\
