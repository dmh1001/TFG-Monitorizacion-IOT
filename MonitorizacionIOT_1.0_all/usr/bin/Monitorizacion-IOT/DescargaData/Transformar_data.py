import json
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from Utilidades.Transformador_sensor_data import *

class Tratador_ficheros_JSON:

    def leer(ruta):
        with open(ruta,"rb") as file:
            data = json.load(file)
            return data



if __name__ == "__main__":

    idSensor = sys.argv[1]
    rutaOrigen = sys.argv[2]
    rutaDestino = sys.argv[3]

    data = Tratador_ficheros_JSON.leer(rutaOrigen)
    dataProcesada = Transformador_sensor_data.transformarJSON(data, idSensor)


    with open(rutaDestino,"w") as file:
        for linea in dataProcesada:
            file.write(linea + "\n")
