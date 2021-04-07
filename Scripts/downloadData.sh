#!bin/bash

#
# Versión 2
#
# se ejecuta cada 5 minutos (300 segundos) para un id de sensor concreto
#

user="prtgadmin"
passhash=1679108625  #2067765068
sleepTime=60 #segundos
path="/home/elk/DownloadSensorData"
IP_PRTG="192.168.0.28:80"

while true
do

        listIdSensores="1003 1006" # TODO: los ids se tendran que almacenar en otro sitio

        for idSensor in $listIdSensores
        do
                sdate=$(date +"%Y-%m-%d-%H-%M-%S" -d '30 minutes ago')
                edate=$(date +"%Y-%m-%d-%H-%M-%S")

                if [ -f $path/tempData"$idSensor".json ]
                then
                        curl -o $path/logs/historic"$idSensor"_2.json $IP_PRTG'/api/historicdata.json?id='$idSensor'&avg=0&usecaption=1&sdate='$sdate'&edate='$edate'&username='$user'&passhash='$passhash

                        $path/transformaSensorData /$path/logs/historic"$idSensor"_2.json $idSensor > $path/tempData"$idSensor"_2.json
                        grep -xvf $path/tempData"$idSensor".json $path/tempData"$idSensor"_2.json > $path/load/load"$idSensor".json
                        #grep -xvf $PATH/tempData"$idSensor".json </home/elk/transformaSensorData /$PATH/logs/historic"$idSensor"_2.json $idSensor > $PATH/load"$idSensor".json
                        bash $path/load_sensor_data.sh $path/load/load"$idSensor".json
                        cat $path/tempData"$idSensor"_2.json > $path/tempData"$idSensor".json
                        rm $path/logs/historic"$idSensor".json
                else
                        curl -o $path/logs/historic"$idSensor".json $IP_PRTG'/api/historicdata.json?id='$idSensor'&avg=0&usecaption=1&sdate='$sdate'&edate='$edate'&username='$user'&passhash='$passhash

                        $path/transformaSensorData $path/logs/historic"$idSensor".json $idSensor > $path/tempData"$idSensor".json
                        bash $path/load_sensor_data.sh $path/tempData"$idSensor".json

                        rm $path/logs/historic"$idSensor".json
                fi

        done
        sleep $sleepTime
done
