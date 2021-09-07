import os
import sys
import re

PACKAGE_PARENT = '..'
PATH=os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(PATH, PACKAGE_PARENT)))

from Modelo import *

from Utilidades.Extractor import *
from Utilidades.Campos import *

if __name__ == "__main__":

    idSensor = sys.argv[1]
    fecha_inicial = datetime.strptime(sys.argv[2],'%d/%m/%Y  %H:%M:00')
    horizonte = int(sys.argv[3])

    modelos = [_ for _ in os.listdir(PATH + "/modelos/") if _.endswith("_"+str(idSensor)+".pickle")]

    if(len(modelos) == 1):
        nombreModelo = modelos[0]
        print(nombreModelo)

        try:
            tipoModelo = re.sub("model","",nombreModelo).split("_")[0]

            if(tipoModelo == "Detretor"):
                model = Persistencia_modelo.cargar(PATH + "/modelos/" + nombreModelo)
                modelo = Modelo_Detrender(idSensor)
                modelo.cargar(model)
            if(tipoModelo == "SNARIMAX"):

                model = Persistencia_modelo.cargar(PATH + "/modelos/" + nombreModelo)
                modelo = Modelo_SNARIMAX(idSensor)
                modelo.cargar(model)


            datosPredichos = modelo.predecir(fecha_inicial, horizonte)

        except Exception as e:
            print("Ha ocurrido un error " + str(e))

        lines = []

        for fecha, valor in datosPredichos.items():
            lines.append(Generador_lineas.generar_linea(idSensor, fecha,{Campos.PREDICCION : valor}))

        with open(PATH + '/pred.json', "w") as file:
            for pred in lines:
                file.write(pred + "\n")
    elif(len(modelos) > 1):
        print("hay mas de un modelo para el sensor " + str(idSensor))

    elif(len(modelos) == 0):
        print("No hay ningún modelo para el sensor " + str(idSensor))
