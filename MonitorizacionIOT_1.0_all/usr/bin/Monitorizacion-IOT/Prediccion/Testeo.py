
import os
import sys

PACKAGE_PARENT = '..'
PATH = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(PATH, PACKAGE_PARENT)))


from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

from Utilidades.Campos import *
from Utilidades.Extractor import *

from math import sqrt

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score


class Testeo:

    def __init__(self, idSensor):
        self.idSensor = idSensor


    def _obtener_valores(self,fecha_inicio, fecha_final):

        realVals = []
        predictVals = []

        real = Extractor.extraer_data(self.idSensor,fecha_inicio, fecha_final ,Campos.VALOR)
        pred = Extractor.extraer_data(self.idSensor,fecha_inicio, fecha_final ,Campos.PREDICCION)

        time = datetime.strptime(fecha_inicio, '%d/%m/%Y %H:%M:%S')
        timeEnd = datetime.strptime(fecha_final, '%d/%m/%Y %H:%M:%S')

        while time <= timeEnd:
            try:
                assert(pred[time])
                assert(real[time])

                predictVals.append(pred[time])
                realVals.append(real[time])

            except:
                pass

            time = time + relativedelta(minutes=1)

        return realVals, predictVals

    def metrica_RMSE(self, fecha_inicio, fecha_final):

        realVals, predictVals = self._obtener_valores(fecha_inicio, fecha_final)
        return sqrt(mean_squared_error(realVals, predictVals))


    def metrica_MAE(self, fecha_inicio, fecha_final):

        realVals, predictVals = self._obtener_valores(fecha_inicio, fecha_final)
        return mean_absolute_error(realVals, predictVals)


    def metrica_MSE(self, fecha_inicio, fecha_final):

        realVals, predictVals = self._obtener_valores(fecha_inicio, fecha_final)
        return mean_squared_error(realVals, predictVals)


    def metrica_R2(self, fecha_inicio, fecha_final):

        realVals, predictVals = self._obtener_valores(fecha_inicio, fecha_final)
        return r2_score(realVals, predictVals)

