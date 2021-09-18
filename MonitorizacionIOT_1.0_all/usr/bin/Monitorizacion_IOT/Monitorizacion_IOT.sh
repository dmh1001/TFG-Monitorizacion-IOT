#!bin/bash

#
# Versión 1
#
# se ejecuta cada  minutos (60 segundos) para un id de sensor concreto
#


# Usuario y passhash de PRTG
usuario_PRTG=""
passhash_PRTG=

IP_PRTG=""

# Tiempo de espera entre cada bucle. Indica cada cuanto se realiza la recogida de Datos, entrenamiento y predicción 
repeticion_ciclo=60 #segundos

# Minutos que se quiere predecir.
horizonte_prediccion=360	 # en minutos	

# Lista de ids de los sensores a 
lista_id_sensores=""


primera_ejecucion=0
path="/usr/bin/Monitorizacion_IOT"


while true
do

	fecha_inicio=$(date +"%Y-%m-%d-%H-%M-00" -d '30 minutes ago')
        fecha_fin=$(date +"%Y-%m-%d-%H-%M-00")

        if [ $primera_ejecucion -eq 0 ]
        then
                fecha_inicio_algoritmo=$(date +"%d/%m/%Y %H:%M:00" -d '30 minutes ago')
                fecha_fin_algoritmo=$(date +"%d/%m/%Y %H:%M:00")

                let primera_ejecucion=1
        else
                fecha_inicio_algoritmo=$(date +"%d/%m/%Y %H:%M:00" -d "$repeticion_ciclo"'seconds ago')
                fecha_fin_algoritmo=$(date +"%d/%m/%Y %H:%M:00")
        fi	
        
	for id_sensor in $lista_id_sensores
        do

		$path/Gestion_datos/Descargar_data.sh "$usuario_PRTG" "$passhash_PRTG" "$IP_PRTG" "$id_sensor" "$fecha_inicio" "$fecha_fin"	


		# Entrenamiento

		python3 $path/Prediccion/Realizar_entrenamiento.py "$id_sensor" "$fecha_inicio_algoritmo" "$fecha_fin_algoritmo" 

                bash $path/Gestion_datos/Load_sensor_data.sh $path/Gestion_datos/TempData_entrenamiento/tempData_entrenamiento"$id_sensor".json

		# Predicción

                bash $path/Gestion_datos/Borrar_datos_predicciones.sh "$id_sensor" $horizonte_prediccion

                python3 $path/Prediccion/Realizar_prediccion.py "$id_sensor" "$fecha_fin_algoritmo" $horizonte_prediccion

                bash $path/Gestion_datos/Load_sensor_data.sh $path/Gestion_datos/TempData_prediccion/tempData_prediccion"$id_sensor".json


        done
   	sleep $repeticion_ciclo

done

