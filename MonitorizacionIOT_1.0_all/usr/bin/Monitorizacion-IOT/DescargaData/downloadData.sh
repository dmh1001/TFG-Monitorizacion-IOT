#!bin/bash

#
# Versión 1
#
# se ejecuta cada  minutos (60 segundos) para un id de sensor concreto
#

usuario="prtgadmin"
passhash=1331387211
tiempoEspera=60 #segundos
path="/usr/bin/DescargaData"
IP_PRTG="192.168.0.26:80"
primeraEjecucion=true


while true
do
        listaIdSensores="2051" # TODO: los ids se tendran que almacenar en otro sitio

        for idSensor in $listaIdSensores
        do
                fechaInicio=$(date +"%Y-%m-%d-%H-%M-00" -d '30 minutes ago')
                fechaFin=$(date +"%Y-%m-%d-%H-%M-00")

                if [ $primeraEjecucion = true ]
                then
                        fechaInicioAlgoritmo=$(date +"%d/%m/%Y %H:%M:00" -d '30 minutes ago')
                        fechaFinAlgoritmo=$(date +"%d/%m/%Y %H:%M:00")

                        let primeraEjecucion=false
                else
                        fechaInicioAlgoritmo=$fechaFinAlgoritmo
                        fechaFinAlgoritmo=$(date +"%d/%m/%Y %H:%M:00")

                fi

                if [ -f $path/tempData"$idSensor".json ]
                then

                       
                        curl -o $path/logs/historic"$idSensor"_2.json $IP_PRTG'/api/historicdata.json?id='$idSensor'&avg=0&usecaption=1&sdate='$fechaInicio'&edate='$fechaFin'&username='$usuario'&passhash='$passhash

                        $path/transformaSensorData /$path/logs/historic"$idSensor"_2.json $idSensor > $path/tempData"$idSensor"_2.json
                        grep -xvf $path/tempData"$idSensor".json $path/tempData"$idSensor"_2.json > $path/load/load"$idSensor".json

                        bash $path/load_sensor_data.sh $path/load/load"$idSensor".json

                        cat $path/tempData"$idSensor"_2.json > $path/tempData"$idSensor".json
                        rm $path/logs/historic"$idSensor"_2.json
                else
                        
                        curl -o $path/logs/historic"$idSensor".json $IP_PRTG'/api/historicdata.json?id='$idSensor'&avg=0&usecaption=1&sdate='$fechaInicio'&edate='$fechaFin'&username='$usuario'&passhash='$passhash

                        $path/transformaSensorData $path/logs/historic"$idSensor".json $idSensor > $path/tempData"$idSensor".json

                        bash $path/load_sensor_data.sh $path/tempData"$idSensor".json

                        rm $path/logs/historic"$idSensor".json
                fi

                sleep 40
                #Entremaniento modelo

                minutosPrediccion=60

                python3 $path/../Prediccion/entrenamientoModelo.py "$fechaInicioAlgoritmo" "$fechaFinAlgoritmo" "$idSensor"

                bash $path/load_sensor_data.sh $path/../Prediccion/entrenamientoData.json

                bash $path/borrarDatosPredicciones.sh $idSensor 120

                python3 $path/../Prediccion/prediccion.py "60" "$idSensor"

                bash $path/load_sensor_data.sh $path/../Prediccion/pred.json


        done

        a=$(($tiempoEspera - 40))

        sleep $a

done

