from river import compose
from river import linear_model
from river import preprocessing
from river import optim
from river import time_series

import os

from Extractor import *
from Campos import *
from Persistencia_modelo import *
from Generador_lineas import *

from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

import abc
from abc import ABC

PATH="/usr/bin/Prediccion"

class Modelo(ABC):

    def __init__(self, idSensor):
         self.idSensor = idSensor

    @abc.abstractmethod
    def _inicializar(self):
        return

    @abc.abstractmethod
    def entrenar(self, fecha_inicio, fecha_fin):
        return

    @abc.abstractmethod
    def predecir(self, minutos):
        return

    def _get_ordinal_date(x):
        return {'ordinal_date': x.hour * 60 + x.minute}

class Modelo_SNARIMAX(Modelo):

    def __init__(self, idSensor):
        Modelo.__init__(self, idSensor)
        self.nombreModelo = PATH + '/modelos/modelSNARIMAX_' + str(idSensor) + '.pickle'

        if os.path.exists(self.nombreModelo):
            self.modelo = Persistencia_modelo.cargar(self.nombreModelo)
        else:
            self.modelo = self._inicializar()

    def _inicializar(self):

        extract_features = compose.TransformerUnion(
            Modelo._get_ordinal_date,
        )

        model = (
            extract_features |
            time_series.SNARIMAX(
                p=0,
                d=0,
                q=2,
                m=30,
                sp=6,
                sq=10,
                regressor=(
                    preprocessing.StandardScaler() |
                    linear_model.LinearRegression(
                        intercept_init=12,
                        optimizer=optim.SGD(0.01),
                        intercept_lr=0.3
                    )
                )
            )
        )

        return model
    def entrenar(self, fecha_inicio, fecha_fin):

        predLines = []
        dates =[]

        for fecha, valor  in Extractor.extraer_data(self.idSensor, fecha_inicio, fecha_fin, Campos.VALOR).items():


            # Obtain the prior prediction and update the model in one go
            y_pred = self.modelo.forecast(horizon=1, xs=[fecha])
            predLine = Generador_lineas.generar_linea(self.idSensor, Campos.ENTRENAMIENTO, fecha, round(y_pred[0],2))

            if( type(valor) == type('')):
                self.modelo.learn_one(fecha, 0)
                # Update the error metric
            else:
                self.modelo.learn_one(fecha, valor)
                # Update the error metric

            # Store the true value and the prediction

            dates.append(fecha)

            predLines.append(predLine)

        with open(PATH + '/entrenamientoData.json', "w") as file:
            for pred in predLines:
                file.write(pred + "\n")


        Persistencia_modelo.guardar(self.modelo, self.nombreModelo)
            
    def predecir(self, horizonte):

        lista_preds = []
        futuro = []
        dates = []

        fecha = datetime.now().strftime('%Y-%m-%d  %H:%M:00')
        fecha = datetime.strptime(fecha, '%Y-%m-%d  %H:%M:00')

        for dia in range(0, horizonte):

            fecha = fecha + relativedelta(minutes=1)
            futuro.append(fecha)
            dates.append(fecha)

        forecast = self.modelo.forecast(horizon=horizonte, xs=futuro)

        for i in range(len(forecast)):
            predLine = Generador_lineas.generar_linea(self.idSensor, Campos.PREDICCION, dates[i], round(forecast[i],2))
            lista_preds.append(predLine)

        with open(PATH + '/pred.json', "w") as file:
            for pred in lista_preds:
                file.write(pred + "\n")

                                                                           