from river import compose
from river import linear_model
from river import preprocessing
from river import metrics
import math
from river import optim
from river import time_series
from river import datasets
import subprocess

import json
import os

#import calendar
from extractorData import *
import types
import sys

import pickle
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta


PATH="/usr/bin/Prediccion"

def get_ordinal_date(x):
    return {'ordinal_date': x.toordinal()}

'''
def get_month_distances(x):
    return {
        calendar.month_name[month]: math.exp(-(x.month - month) ** 2)
        for month in range(1, 13)
    }
'''

def get_hour(x):
    return x.minute

class Prediccion:

    def __init__(self, idSensor):
        self.idSensor = idSensor

    def _generar_linea(self, campo, date, y_pred):
        return "{\"sensorId\":\"" + str(self.idSensor) + "\",\"datetime\":\"" + date.strftime("%d/%m/%Y %H:%M:%S") + "\",\"reading\":{\""+campo+"\":" + str(y_pred) + "}}"

    def inicializar_modelo(self):


        model = compose.Pipeline(
            ('features', compose.TransformerUnion(
                ('ordinal_date', compose.FuncTransformer(get_ordinal_date))
                #('hour', compose.FuncTransformer(get_hour))
            )),
            ('scale', preprocessing.StandardScaler()),
            ('lin_reg', linear_model.LinearRegression(
                intercept_lr=0,
                optimizer=optim.SGD(0.001)
            ))
        )

        extract_features = compose.TransformerUnion(get_ordinal_date)

        scale = preprocessing.StandardScaler()

        learn = linear_model.LinearRegression(
            intercept_lr=0,
            optimizer=optim.SGD(0.001)
        )

        model = extract_features | scale | learn
        model = time_series.Detrender(regressor=model, window_size=12)


        return model


    '''
    Método que carga el modelo en un ficharo
    '''
    def cargar_modelo(self):

        try:
            with open(PATH + '/modelos/model_'+ str(self.idSensor) +'.pickle', "rb") as file:
                return pickle.load(file)
        except FileNotFoundError as e:
            print("Error, modelo no encontrado")

    '''
    Método que guarda el modelo en un ficharo
    '''
    def guardar_modelo(self, model):
        with open(PATH + '/modelos/model_' + str(self.idSensor) + '.pickle',"wb") as file:
            pickle.dump(model, file)


def entrenamiento_modelo(self, fecha_inicio, fecha_fin):

        predLines = []
        dates =[]
        y_preds = []
        y_trues = []

        metric = metrics.Rolling(metrics.MAE(), 12)

        if os.path.exists(PATH + '/modelos/model_'+ str(self.idSensor) +'.pickle'):
            modelo = self.cargar_modelo()
        else:
            modelo = self.inicializar_modelo()

        for fecha, valor  in extractorData.extraer_data(self.idSensor, fecha_inicio, fecha_fin):

            # Obtain the prior prediction and update the model in one go
            y_pred = modelo.predict_one(fecha)


            predLine = self._generar_linea("Entrenamiento", fecha, y_pred)


            if( type(valor) == type('')):
                modelo.learn_one(fecha, 0)

                # Update the error metric
                metric.update(0, y_pred)

            else:
                modelo.learn_one(fecha, valor)

                # Update the error metric
                metric.update(valor, y_pred)

            # Store the true value and the prediction
            dates.append(fecha)
            y_trues.append(valor)
            y_preds.append(y_pred)

            predLines.append(predLine)


        with open(PATH + '/entrenamientoData.json', "w") as file:
            for pred in predLines:
                file.write(pred + "\n")

        self.guardar_modelo(modelo)

def prediccion(self, minutos):

        lista_preds = []

        fecha = datetime.now()
        fecha = fecha.strftime('%Y-%m-%d  %H:%M:00')
        fecha = datetime.strptime(fecha, '%Y-%m-%d  %H:%M:00')

        if os.path.exists(PATH + '/modelos/model_'+ str(self.idSensor) +'.pickle'):
            modelo = self.cargar_modelo()
        else:
            modelo = self.inicializar_modelo()

        for dia in range(0, minutos):

            fecha = fecha + relativedelta(minutes=1)
            pred = modelo.predict_one(fecha)


            predLine = self._generar_linea("Prediccion", fecha, pred)
            lista_preds.append(predLine)

        with open(PATH + '/pred.json', "w") as file:
            for pred in lista_preds:
                file.write(pred + "\n")

if __name__ == "__main__":

    p = Prediccion(sys.argv[3])
    p.entrenamiento_modelo(sys.argv[1], sys.argv[2])



