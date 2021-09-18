import json
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from Utilidades.Tratamiento_sensor_data import *


if __name__ == "__main__":
    
    idSensor = sys.argv[1] 
    rutaOrigen = sys.argv[2]
    rutaDestino = sys.argv[3]
    
    tratador = Tratamiento_sensor_data()

    data = tratador.leerJSON(rutaOrigen)
    dataProcesada = tratador.transformarJSON(data, idSensor)
    
    
    with open(rutaDestino,"w") as file:
        for linea in dataProcesada:
            file.write(linea + "\n")

