from river import compose
from river import linear_model
from river import preprocessing
import math
from river import optim
from river import time_series

import os
import sys

PACKAGE_PARENT = '..'
PATH=os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(PATH, PACKAGE_PARENT)))

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
    def inicializar(self):
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
        self.tipo = "SNARIMAX"
        self.nombre = PATH + '/modelos/model'+self.tipo+'_' + str(idSensor) + '.pickle'
        self.modelo = None

    def cargar(self, modelo):
        self.modelo = modelo

    def inicializar(self, p = 0, d = 0, q = 0, m = 1, sp = 0, sq = 0, intercept_init = 0, sgd = 0, intercerpt_lr = 0):
        self.p = p
        self.d = d
        self.q = q
        self.m = m
        self.sp = sp
        self.sq = sq

        self.intercept_init = intercept_init
        self.sgd = sgd
        self.intercerpt_lr = intercerpt_lr

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

        self.modelo = model

    def entrenar(self, datos):

        datosEntrenamiento = {}

        for fecha, valor  in datos.items():

            y_pred = self.modelo.forecast(horizon=1, xs=[fecha])
            datosEntrenamiento[fecha] = round(y_pred[0],2)
            self.modelo.learn_one(fecha, valor)

        return datosEntrenamiento

    def predecir(self, fecha_inicial, horizonte):

        datosPredichos = {}
        futuro = []
        dates = []

        fecha = fecha_inicial

        for dia in range(0, horizonte):

            fecha = fecha + relativedelta(minutes=1)
            futuro.append(fecha)
            dates.append(fecha)

        forecast = self.modelo.forecast(horizon=horizonte, xs=futuro)

        for i in range(len(forecast)):

            datosPredichos[dates[i]] = round(forecast[i],2)

        return datosPredichos

    def __str__(self):
        return "Modelo de típo: %s para el sensor: %s" %(self.tipo, self.idSensor)


class Modelo_Detrender(Modelo):

    def __init__(self, idSensor):
        Modelo.__init__(self, idSensor)
        self.tipo = "Detrender"
        self.nombre = PATH + '/modelos/model'+self.tipo+'_' + str(idSensor) + '.pickle'
        self.modelo = None

    def cargar(self, modelo):
        self.modelo = modelo

    def inicializar(self, sgd, window = None, intercept_lr = 0):

        self.window = window
        self.intercept_lr = intercept_lr
        self.sgd = sgd


        extract_features = compose.TransformerUnion(Modelo._get_ordinal_date)

        scale = preprocessing.StandardScaler()

        learn = linear_model.LinearRegression(
            intercept_lr=self.intercept_lr,
            optimizer=optim.SGD(self.sgd)
        )

        model = extract_features | scale | learn

        model = time_series.Detrender(regressor=model, window_size=self.window)

        return model

    def entrenar(self, datos):

        datosEntrenamiento = {}

        for fecha, valor  in datos.items():

            y_pred = self.modelo.predict_one(fecha)
            datosEntrenamiento[fecha] = round(y_pred,2)

            self.modelo.learn_one(fecha, valor)

        return datosEntrenamiento

    def predecir(self, fecha_inicial, horizonte):

        datosPredichos = {}

        fecha = fecha_inicial
        for dia in range(0, horizonte):
            fecha = fecha + relativedelta(minutes=1)
            pred = self.model.predict_one(fecha)
            datosPredichos[fecha] = pred

        return datosPredichos

    def __str__(self):
        return "Modelo de típo: %s para el sensor: %s" %(self.tipo, self.idSensor)








