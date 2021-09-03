from datetime import date
from datetime import datetime

class Generador_lineas:
    def generar_linea(idSensor, campo, date, y_pred):
        return "{\"sensorId\":\"" + str(idSensor) + "\",\"datetime\":\"" + date.strftime("%d/%m/%Y %H:%M:%S") + "\",\"reading\":{\""+campo+"\":" + str(y_pred) + "}}"
        