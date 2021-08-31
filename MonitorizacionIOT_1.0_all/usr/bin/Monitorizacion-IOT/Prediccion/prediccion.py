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
        return {'ordinal_date': x.hour * 60 + x.minute
}

class Prediccion:

    def __init__(self, idSensor):
        self.idSensor = idSensor

    def _generar_linea(self, campo, date, y_pred):
        return "{\"sensorId\":\"" + str(self.idSensor) + "\",\"datetime\":\"" + date.strftime("%d/%m/%Y %H:%M:%S") + "\",\"reading\":{\""+campo+"\":" + str(y_pred) + "}}"

    def inicializar_modelo(self):

        extract_features = compose.TransformerUnion(
            get_ordinal_date,
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
            y_pred = modelo.forecast(horizon=1, xs=[fecha])
            predLine = self._generar_linea("Entrenamiento", fecha, y_pred[0])

            if( type(valor) == type('')):
                modelo.learn_one(date, 0)
                # Update the error metric
                metric.update(0, y_pred[0])
            else:
                modelo.learn_one(fecha, valor)
                # Update the error metric
                metric.update(valor, y_pred[0])

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
        horizonte = minutos
        futuro = []
        dates = []

        fecha = datetime.now().strftime('%Y-%m-%d  %H:%M:00')
        fecha = datetime.strptime(fecha, '%Y-%m-%d  %H:%M:00')

        if os.path.exists(PATH + '/modelos/model_'+ str(self.idSensor) +'.pickle'):
            modelo = self.cargar_modelo()
        else:
            modelo = self.inicializar_modelo()

        for dia in range(0, horizonte):

            fecha = fecha + relativedelta(minutes=1)
            futuro.append(fecha)
            dates.append(fecha)

        forecast = modelo.forecast(horizon=horizonte, xs=futuro)

        for i in range(len(forecast)):
            predLine = self._generar_linea("Prediccion", dates[i], forecast[i])
            lista_preds.append(predLine)

        with open(PATH + '/pred.json', "w") as file:
            for pred in lista_preds:
                file.write(pred + "\n")


if __name__ == "__main__":

    p = Prediccion(sys.argv[3])
    p.entrenamiento_modelo(sys.argv[1], sys.argv[2])

