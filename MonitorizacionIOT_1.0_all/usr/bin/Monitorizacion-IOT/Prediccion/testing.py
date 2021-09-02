from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

from Campos import *
from extractorData import *

import sys

from math import sqrt
from sklearn.metrics import mean_squared_error

PATH="/usr/bin/Prediccion"

class Testeo:
    def prediccion_RMSE(idSensor, fecha_inicio, fecha_final):
        real = extractorData.extraer_data(idSensor,fecha_inicio, fecha_final ,Campos.VALOR)
        pred = extractorData.extraer_data(idSensor,fecha_inicio, fecha_final ,Campos.PREDICCION)

        time = datetime.strptime(fecha_inicio, '%d/%m/%Y %H:%M:%S')
        timeEnd = datetime.strptime(fecha_final, '%d/%m/%Y %H:%M:%S')

        realVals = []
        predinctVals = []

        while time <= timeEnd:
            try:
                print(pred[time])
                print(real[time])

                predinctVals.append(pred[time])
                realVals.append(real[time])
            except:
                pass

            time = time + relativedelta(minutes=1)

        print(realVals)
        rmse = sqrt(mean_squared_error(realVals, predinctVals))

        return rmse


if __name__ == "__main__":

    idSensor = sys.argv[1]
    fecha_inicio = sys.argv[2]
    fecha_final = sys.argv[3]

    rmse = Testeo.prediccion_RMSE(idSensor, fecha_inicio, fecha_final)

    with open(PATH + '/testeo.txt', "a") as file:
        file.write(str(fecha_inicio) + " - " + str(fecha_final) + " : " + str(rmse) )

