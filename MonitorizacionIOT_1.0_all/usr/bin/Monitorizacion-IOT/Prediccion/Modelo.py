PACKAGE_PARENT = '..'
PATH=os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(PATH, PACKAGE_PARENT)))

from river import compose
from river import linear_model
from river import preprocessing
import math
from river import optim
from river import time_series

import os
import sys

from Utilidades.Extractor import *
from Utilidades.Campos import *
from Persistencia_modelo import *
from Utilidades.Generador_lineas import *

from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

import abc
from abc import ABC

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

        self.p = 0
        self.d = 0
        self.q = 2
        self.m = 30
        self.sp = 6
        self.sq = 10

        self.intercept_init = 12
        self.sgd = 0.01
        self.intercerpt_lr = 0.3

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
                p=self.p,
                d=self.d,
                q=self.q,
                m=self.m,
                sp=self.sp,
                sq=self.sq,
                regressor=(
                    preprocessing.StandardScaler() |
                    linear_model.LinearRegression(
                        intercept_init= self.intercept_init,
                        optimizer=optim.SGD(self.sgd),
                        intercept_lr= self.intercerpt_lr
                    )
                )
            )
        )

        return model

    def entrenar(self, fecha_inicio, fecha_fin):

        predLines = []
        dates =[]

        for fecha, valor  in Extractor.extraer_data(self.idSensor, fecha_inicio, fecha_fin, Campos.VALOR).items():

            y_pred = self.modelo.forecast(horizon=1, xs=[fecha])
            predLine = Generador_lineas.generar_linea(self.idSensor, Campos.ENTRENAMIENTO, fecha, round(y_pred[0],2))

            if( type(valor) == type('')):
                self.modelo.learn_one(fecha, 0)
            else:
                self.modelo.learn_one(fecha, valor)

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

class Modelo_Detrender(Modelo):

    def __init__(self, idSensor):
        Modelo.__init__(self, idSensor)
        self.nombreModelo = PATH + '/modelos/modelDetrender_' + str(idSensor) + '.pickle'

        self.Window = 12
        self.intercept_lr = 0
        self.sgd = 0.03

        if os.path.exists(self.nombreModelo):
            self.modelo = Persistencia_modelo.cargar(self.nombreModelo)
        else:
            self.modelo = self._inicializar()

    def _inicializar(self):


        extract_features = compose.TransformerUnion(Modelo._get_ordinal_date)

        scale = preprocessing.StandardScaler()

        learn = linear_model.LinearRegression(
            intercept_lr=self.intercept_lr,
            optimizer=optim.SGD(self.sgd)
        )

        model = extract_features | scale | learn

        model = time_series.Detrender(regressor=model, window_size=self.window)


        return model

    def entrenar(self, fecha_inicio, fecha_fin):

        predLines = []
        dates =[]

        for fecha, valor  in Extractor.extraer_data(self.idSensor, fecha_inicio, fecha_fin, Campos.VALOR).items():

            y_pred = self.modelo.predict_one(fecha)
            predLine = Generador_lineas.generar_linea(self.idSensor, Campos.ENTRENAMIENTO, fecha, round(y_pred,2))

            if( type(valor) == type('')):
                self.modelo.learn_one(fecha, 0)
            else:
                self.modelo.learn_one(fecha, valor)

            dates.append(fecha)
            predLines.append(predLine)

        with open(PATH + '/entrenamientoData.json', "w") as file:
            for pred in predLines:
                file.write(pred + "\n")


        Persistencia_modelo.guardar(self.modelo, self.nombreModelo)

    def predecir(self, horizonte):

        lista_preds = []

        fecha = datetime.now().strftime('%Y-%m-%d  %H:%M:00')
        fecha = datetime.strptime(fecha, '%Y-%m-%d  %H:%M:00')

        for dia in range(0, horizonte):

            fecha = fecha + relativedelta(minutes=1)
            pred = self.model.predict_one(fecha)

            predLine = Generador_lineas.generar_linea(self.idSensor, Campos.PREDICCION, fecha, round(pred,2))
            lista_preds.append(predLine)

        with open(PATH + '/pred.json', "w") as file:
            for pred in lista_preds:
                file.write(pred + "\n")
                                               