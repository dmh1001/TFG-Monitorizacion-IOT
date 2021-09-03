import sys
from Testeo import *

if __name__ == "__main__":

    idSensor = sys.argv[1]
    fecha_inicio = sys.argv[2]
    fecha_final = sys.argv[3]

    rmse = Testeo.prediccion_RMSE(idSensor, fecha_inicio, fecha_final)

    with open(PATH + '/testeo.txt', "a") as file:
        file.write(str(fecha_inicio) + " - " + str(fecha_final) + " : " + str(rmse) )
