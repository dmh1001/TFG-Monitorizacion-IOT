from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

from Campos import *
from Extractor import *

from math import sqrt
from sklearn.metrics import mean_squared_error

PATH="/usr/bin/Prediccion"

class Testeo:
    def prediccion_RMSE(idSensor, fecha_inicio, fecha_final):
        real = Extractor.extraer_data(idSensor,fecha_inicio, fecha_final ,Campos.VALOR)
        pred = Extractor.extraer_data(idSensor,fecha_inicio, fecha_final ,Campos.PREDICCION)


        time = datetime.strptime(fecha_inicio, '%d/%m/%Y %H:%M:%S')
        timeEnd = datetime.strptime(fecha_final, '%d/%m/%Y %H:%M:%S')

        realVals = []
        predinctVals = []

        while time <= timeEnd:
            try:
                assert(pred[time])
                assert(real[time])

                predinctVals.append(pred[time])
                realVals.append(real[time])
            except:
                pass

            time = time + relativedelta(minutes=1)

        rmse = sqrt(mean_squared_error(realVals, predinctVals))

        return rmse
