#!/bin/bash

path="/usr/bin/Predeicion"
minutos = 120

while true
do

        listaIdSensores = "2051"

        for idSensor in $listaIdSensores
        do
                fechaInicio=$(date +"%d/%m/%Y %H:%M:00" -d $minutos ' minutes ago')
                fechaFinal=$(date +"%d/%m/%Y %H:%M:00")

                python3 $path/testing.py $idSensor $fechaInicio $fechaFinal
        done
done

