#!bin/bash

#
# Versión 1
#
# se ejecuta cada 5 minutos (300 segundos) para un id de sensor concreto
#

user="prtgadmin"
passhash=2067765068
idSensor=1006


while true
do
        sdate=$(date +"%Y-%m-%d-%H-%M-%S" -d '30 minutes ago')
        edate=$(date +"%Y-%m-%d-%H-%M-%S")

        curl -o /home/elk/logs/historic.log '192.168.0.21:80/api/historicdata.json?id='$idSensor'&avg=0&usecaption=1&sdate='$sdate'&edate='$edate'&username='$user'&passhash='$passhash
        sleep 300
done

