#!/bin/bash

usuario_PRTG=$1
passhash_PRTG=$2
IP_PRTG=$3

id_sensor=$4


fecha_inicio=$5
fecha_fin=$6


path="/usr/bin/Monitorizacion_IOT/Gestion_datos"

# Función que descarga datos de PRTG

# $1 : idSensor
# $2 : fecha inicio
# $3 : fecha fin
# $4 : volcado datos
function descarga_datos_PRTG(){

        curl -o "$4" $IP_PRTG'/api/historicdata.json?id='$1'&avg=0&usecaption=1&sdate='$2'&edate='$3'&username='$usuario_PRTG'&passhash='$passhash_PRTG
}

# Función que transforma los datos recogidos en PRTG y los transforma en datos legibles
# para ElasticSearch

# $1 : idSensor
# $2 : nombre fichero entrada

function transformar_datos(){

        $path/../Utilidades/Transforma_sensor_data $2 $1

}

# Función que compara dos ficheros y devuelve las lineas que no tienen en comun.

# $1 : primer fichero
# $2 : segundo fichero
# #3 : id sensor
function comparar_ficheros(){
        grep -xvf $1 $2 > $path/load/load"$3".json
}



if [ -f $path/TempData_sensores/tempData"$id_sensor".json ]
then

        descarga_datos_PRTG "$id_sensor" "$fecha_inicio" "$fecha_fin" $path/logs/historic"$id_sensor"_2.json

        python3 $path/../Utilidades/Transformar_data.py $id_sensor /$path/logs/historic"$id_sensor"_2.json $path/TempData_sensores/tempData"$id_sensor"_2.json

        comparar_ficheros $path/TempData_sensores/tempData"$id_sensor".json $path/TempData_sensores/tempData"$id_sensor"_2.json "$id_sensor"

        bash $path/Load_sensor_data.sh $path/load/load"$id_sensor".json

        cat $path/TempData_sensores/tempData"$id_sensor"_2.json > $path/TempData_sensores/tempData"$id_sensor".json
        rm $path/logs/historic"$id_sensor"_2.json

else
	
        descarga_datos_PRTG "$id_sensor" "$fecha_inicio" "$fecha_fin" $path/logs/historic"$id_sensor".json
       	python3 $path/../Utilidades/Transformar_data.py "$id_sensor" /$path/logs/historic"$id_sensor".json $path/TempData_sensores/tempData"$id_sensor".json
       	bash $path/Load_sensor_data.sh $path/TempData_sensores/tempData"$id_sensor".json

fi
