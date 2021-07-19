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

import calendar
from extractorData import *
import types
import sys

import pickle
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_ordinal_date(x):
        return {'ordinal_date': x.toordinal()}

def get_month_distances(x):
    return {
        calendar.month_name[month]: math.exp(-(x.month - month) ** 2)
        for month in range(1, 13)
    }


class Prediccion:

    def __init__(self, idSensor):
        self.idSensor = idSensor

    def _generarLinea(self, date, y_pred):
        return "{\"sensorId\":\"" + str(self.idSensor) + "\",\"datetime\":\"" + date.strftime("%d/%m/%Y %H:%M:%S") + "\",\"reading\":{\"Prediction\":" + str(y_pred) + "}}"
    
    def initModel(self):

            model = compose.Pipeline(
                ('features', compose.TransformerUnion(
                    ('ordinal_date', compose.FuncTransformer(get_ordinal_date)),
                    ('month_distances', compose.FuncTransformer(get_month_distances)),
                )),
                ('scale', preprocessing.StandardScaler()),
                ('lin_reg', linear_model.LinearRegression(
                    intercept_lr=0,
                    optimizer=optim.SGD(0.03)
                ))
            )

            extract_features = compose.TransformerUnion(get_ordinal_date, get_month_distances)

            scale = preprocessing.StandardScaler()

            learn = linear_model.LinearRegression(
                intercept_lr=0,
                optimizer=optim.SGD(0.03)
            )

            model = extract_features | scale | learn
            model = time_series.Detrender(regressor=model, window_size=12)

            return model

    '''
    Método que carga el modelo en un ficharo
    '''
    def cargarModelo(self):

        try:
            with open('/home/elk/Prediccion/model_'+ str(self.idSensor) +'.pickle', "rb") as file:
                return pickle.load(file)
        except FileNotFoundError as e:
            print("Error")

    '''
    Método que guarda el modelo en un ficharo
    '''
    def guardarModelo(self, model):
        with open('/home/elk/Prediccion/model_' + str(self.idSensor) + '.pickle',"wb") as file:
            pickle.dump(model, file)

    def evaluate_model(self, fechaInicio, fechaFin):
        predLines = []
        dates =[]
        y_preds = []
        y_trues = []

        metric = metrics.Rolling(metrics.MAE(), 12)

        if os.path.exists('/home/elk/Prediccion/model_'+ str(self.idSensor) +'.pickle'):
            model = self.cargarModelo()
        else:
            model = self.initModel()

        for date, value  in extractorData.extractData(self.idSensor, fechaInicio, fechaFin):

            # Obtain the prior prediction and update the model in one go
            y_pred = model.predict_one(date)

            predLine = self._generarLinea(date, y_pred)

            if( type(value) == type('')):
                model.learn_one(date, 0)

                # Update the error metric
                metric.update(0, y_pred)

            else:
                model.learn_one(date, value)

                # Update the error metric
                metric.update(value, y_pred)

            # Store the true value and the prediction
            dates.append(date)
            y_trues.append(value)
            y_preds.append(y_pred)

            predLines.append(predLine)

            self._subirDatosPredichosElasticSearch(predLines, "prediccionData.json")
            self.guardarModelo(model)
    def prediccionSiguentesDias(self, model, nDias):

            lista_preds = []
            d = datetime.now()

            for dia in range(0,nDias * 1440):

                d = d + relativedelta(minutes=1)

                pred = model.predict_one(d)

                predLine = self._generarLinea(date, pred)
                lista_preds.append(predLine)


                self._subirDatosPredichosElasticSearch(lista_preds, "pred.json")

    '''
    Método que sube los datos predichos a Elasticsearch.
    '''
    def _subirDatosPredichosElasticSearch(self, predLines, nombreFichero):
        with open('/home/elk/Prediccion/' + str(nombreFichero) + '', "w") as file:
            for pred in predLines:
                file.write(pred + "\n")

        os.system("bash /home/elk/DownloadData/load_sensor_data.sh /home/elk/Prediccion/" + str(nombreFichero) + "")



if __name__ == "__main__":

    p = Prediccion("2051")
    p.evaluate_model(sys.argv[1], sys.argv[2])


    #prediccion(model, 1)


