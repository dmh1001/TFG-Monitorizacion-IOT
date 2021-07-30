#/bun/bash

sensorId=$1
minutos=$2

fechaInicio=$(date +"%d/%m/%Y")
horaInicio=$(date +"%H:%M:00")
fechaFin=$(date +"%d/%m/%Y" -d '+ ' $minutos ' minutes')
horaFin=$(date +"%H:%M:00" -d '+ ' $minutos ' minutes')

curl -XPOST -H 'Content-Type: application/json' localhost:9200/_all/_delete_by_query -d '{
"query":

    {
      "bool":
      {
        "must":
        [
          {
            "match":
            {
              "sensorId":'$sensorId'

            }
          },
          {
           "range":
            {
              "datetime" : {
                "gt" : "'$fechaInicio' '$horaInicio'",
                "lte" : "'$fechaFin' '$horaFin'"
            }
            }
          },{
          "exists":
          {
            "field":"Prediccion"
          }
          }
        ]
      }

    }
}'
