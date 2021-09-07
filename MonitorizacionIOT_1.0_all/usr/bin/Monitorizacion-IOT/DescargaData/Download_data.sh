#!bin/bash

#
# Versión 1
#
# se ejecuta cada  minutos (60 segundos) para un id de sensor concreto
#

usuario="prtgadmin"
passhash=1331387211
tiempoEspera=60 #segundos
path="/usr/bin/Monitorizacion_IOT/DescargaData"
IP_PRTG="192.168.0.26:80"
primeraEjecucion=true


listaIdSensores="2051 2052" # TODO: los ids se tendran que almacenar en otro sitio

# Función que descarga datos de PRTG

# $1 : idSensor
# $2 : fecha inicio
# $3 : fecha fin
# $4 : volcado datos
function descarga_datos_PRTG(){

        curl -o "$4" $IP_PRTG'/api/historicdata.json?id='$1'&avg=0&usecaption=1&sdate='$2'&edate='$3'&username='$usuario'&passhash='$passhash
}

# Función que transforma los datos recogidos en PRTG y los transforma en datos legibles
# para ElasticSearch

# $1 : idSensor
# $2 : nombre fichero entrada

function transformar_datos(){

        $path/Transforma_sensor_data $2 $1
}

# Función que compara dos ficheros y devuelve las lineas que no tienen en comun.

# $1 : primer fichero
# $2 : segundo fichero
# #3 : id sensor
function comparar_ficheros(){
        grep -xvf $1 $2 > $path/load/load"$3".json
}



while true
do
        l=$listaIdSensores
        for idSensor in $l
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

                        descarga_datos_PRTG "$idSensor" "$fechaInicio" "$fechaFin" $path/logs/historic"$idSensor"_2.json
                        python3 $path/Transformar_data.py $idSensor /$path/logs/historic"$idSensor"_2.json $path/tempData"$idSensor"_2.json

                        comparar_ficheros $path/tempData"$idSensor".json $path/tempData"$idSensor"_2.json "$idSensor"

                        bash $path/Load_sensor_data.sh $path/load/load"$idSensor".json

                        cat $path/tempData"$idSensor"_2.json > $path/tempData"$idSensor".json
                        rm $path/logs/historic"$idSensor"_2.json
                else
                        descarga_datos_PRTG "$idSensor" $fechaInicio $fechaFin $path/logs/historic"$idSensor".json
                        python3 $path/Transformar_data.py $idSensor /$path/logs/historic"$idSensor".json $path/tempData"$idSensor".json

                        bash $path/Load_sensor_data.sh $path/tempData"$idSensor".json

                        rm $path/logs/historic"$idSensor".json
                fi

                sleep 40
                #Entremaniento modelo

                minutosPrediccion=360

                python3 $path/../Prediccion/Realizar_entrenamiento.py "$idSensor" "$fechaInicioAlgoritmo" "$fechaFinAlgoritmo"

                bash $path/Load_sensor_data.sh $path/../Prediccion/entrenamientoData.json

                bash $path/BorrarDatosPredicciones.sh "$idSensor" $minutosPrediccion

                python3 $path/../Prediccion/Realizar_prediccion.py "$idSensor" "$fechaFinAlgoritmo" $minutosPrediccion

                bash $path/Load_sensor_data.sh $path/../Prediccion/pred.json


        done

        a=$(($tiempoEspera - 40))

        sleep $a

done


