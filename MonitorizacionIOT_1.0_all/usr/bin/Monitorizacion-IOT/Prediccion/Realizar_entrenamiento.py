import os
import sys
import re

PACKAGE_PARENT = '..'
PATH=os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(PATH, PACKAGE_PARENT)))

from Modelo import *

from Utilidades.Extractor import *
from Utilidades.Campos import *
from Persistencia_modelo import *


if __name__ == "__main__":
    idSensor = sys.argv[1]
    fecha_inicio = sys.argv[2]
    fecha_final = sys.argv[3]

    modelos = [_ for _ in os.listdir(PATH + "/modelos/") if _.endswith("_"+str(idSensor)+".pickle")]

    if(len(modelos) == 1):
        nombreModelo = modelos[0]

        try:

            modelo = Persistencia_modelo.cargar(nombreModelo)

            datos = Extractor.extraer_data(idSensor, fecha_inicio, fecha_final, Campos.VALOR)

            datosEntrenamiento = modelo.entrenar(datos)
            Persistencia_modelo.guardar(modelo)

            lines = []

            for fecha, valor in datosEntrenamiento.items():
                lines.append(Generador_lineas.generar_linea(idSensor, fecha,{Campos.ENTRENAMIENTO : valor}))

            with open(PATH + '/tempData_entrenamiento.json', "w") as file:
                for pred in lines:
                    file.write(pred + "\n")

        except Exception as e:
            print("Se ha producido un error: " + str(e) + " \n")


    elif(len(modelos) > 1):
        print("hay mas de un modelo para el sensor " + str(idSensor) + "\n")

    elif(len(modelos) == 0):
        print("No hay ningún modelo para el sensor " + str(idSensor)+ "\n")

