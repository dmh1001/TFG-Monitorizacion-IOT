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

def get_ordinal_date(x):
    return {'ordinal_date': x.toordinal()}

def get_month_distances(x):
    return {
        calendar.month_name[month]: math.exp(-(x.month - month) ** 2)
        for month in range(1, 13)
    }
def evaluate_model(model, fechaInicio, fechaFin):

    metric = metrics.Rolling(metrics.MAE(), 12)

    for date, value  in extractorData.extractData(IdSensor, fechaInicio, fechaFin):

        # Obtain the prior prediction and update the model in one go
        y_pred = model.predict_one(date)

        with open('./home/elk/Prediccion/dates.txt','a') as file:
            file.write(date.strftime("%d/%m/%Y %H:%M:%S") + " " + str(value) + ": " + str(y_pred)+"\n")


        predLine = "{\"sensorId\":\"" + str(IdSensor) + "\",\"datetime\":\"" + date.strftime("%d/%m/%Y %H:%M:%S") + "\",\"reading\":{\"Prediction\":" + str(y_pred) + "}}"

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

def initModel():

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

predLines = []
dates =[]
y_preds = []
y_trues = []
IdSensor = "2051"

if( int(sys.argv[3]) == 1):
    model = initModel()
else:
    with open('/home/elk/Prediccion/model.pickle', "rb") as file:
        model = pickle.load(file)

with open('./home/elk/Prediccion/dates.txt','a') as file:
    file.write("STRART: "+ sys.argv[1] + " " + sys.argv[2] + "\n")

evaluate_model(model, sys.argv[1], sys.argv[2])

with open('./home/elk/Prediccion/dates.txt','a') as file:
    file.write("DONE\n")

with open('./home/elk/Prediccion/predictData.json','w') as file:
    for pred in predLines:
        file.write(pred + "\n")
