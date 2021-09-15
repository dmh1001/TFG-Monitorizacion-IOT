#!bin/bash
#
# Versión 1
#
# se ejecuta cada  minutos (60 segundos) para un id de sensor concreto
#

# Usuario y passhash de PRTG
usuario_PRTG="prtgadmin"
passhash_PRTG=1331387211

IP_PRTG="192.168.0.26:80"

# Tiempo de espera entre cada bucle. Indica cada cuanto se realiza la recogida de Datos, entrenamiento y predicción
repeticion_ciclo=60 #segundos

tiempo_espera=10

# Minutos que se quiere predecir.
horizonte_prediccion=360         # en minutos

# Lista de ids de los sensores a
lista_id_sensores="2051" # TODO: los ids se tendran que almacenar en otro sitio


primera_ejecucion=true
path="/usr/bin/Monitorizacion_IOT"


while true
do

        for id_sensor in $lista_id_sensores
        do
                fecha_inicio=$(date +"%Y-%m-%d-%H-%M-00" -d '30 minutes ago')
                fecha_fin=$(date +"%Y-%m-%d-%H-%M-00")

                if [ $primera_ejecucion = true ]
                then
                        fecha_inicio_algoritmo=$(date +"%d/%m/%Y %H:%M:00" -d '30 minutes ago')
                        fecha_fin_algoritmo=$(date +"%d/%m/%Y %H:%M:00")

                        let primera_ejecucion=false
                else
                        fecha_inicio_algoritmo=$fecha_fin_Algoritmo
                        fecha_fin_algoritmo=$(date +"%d/%m/%Y %H:%M:00")

                fi

                $path/Gestion_datos/Descargar_data.sh "$usuario_PRTG" "$passhash_PRTG" "$IP_PRTG" "$id_sensor" "$fecha_inicio" "$fecha_fin"


                sleep $tiempo_espera

                # Entrenamiento

                if [ -f $path/Prediccion/tempData_entrenamiento.json ]
                then
                        rm $path/Prediccion/tempData_entrenamiento.json
                fi

                python3 $path/Prediccion/Realizar_entrenamiento.py "$id_sensor" "$fecha_inicio_algoritmo" "$fecha_fin_algoritmo"

                bash $path/Gestion_datos/Load_sensor_data.sh $path/Prediccion/tempData_entrenamiento.json

                # Predicción

                if [ -f $path/Prediccion/tempData_prediccion.json ]
                then
                        rm $path/Prediccion/tempData_prediccion.json
                fi

                bash $path/Gestion_datos/Borrar_datos_predicciones.sh "$id_sensor" $horizonte_prediccion

                python3 $path/Prediccion/Realizar_prediccion.py "$id_sensor" "$fecha_fin_algoritmo" $horizonte_prediccion

                bash $path/Gestion_datos/Load_sensor_data.sh $path/Prediccion/tempData_prediccion.json
        done
        sleep $(($repeticion_ciclo - $tiempo_espera ))


done

