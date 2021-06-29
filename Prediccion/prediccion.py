from river import compose
from river import linear_model
from river import preprocessing
from river import metrics
import math
from river import optim
from river import time_series
from river import datasets

import calendar
from extractorData import *
import types

def get_ordinal_date(x):
    return {'ordinal_date': x.toordinal()}

def get_month_distances(x):
    return {
        calendar.month_name[month]: math.exp(-(x.month - month) ** 2)
        for month in range(1, 13)
    }
def evaluate_model(model):

    metric = metrics.Rolling(metrics.MAE(), 12)

    for x, y in extractorData.extractData("2051","21/06/2021 00:00:00", "22/06/2021 00:00:00"):


        print("date: ", x)
        print("true:", y)
        # Obtain the prior prediction and update the model in one go
        y_pred = model.predict_one(x)

        if( type(y) == type('')):
            model.learn_one(x, 0)

            # Update the error metric
            metric.update(0, y_pred)
        else:
            model.learn_one(x, y)

            # Update the error metric
            metric.update(y, y_pred)

        # Store the true value and the prediction
        dates.append(x)
        y_trues.append(y)
        y_preds.append(y_pred)

        
dates =[]
y_preds = []
y_trues = []

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

evaluate_model(model)
