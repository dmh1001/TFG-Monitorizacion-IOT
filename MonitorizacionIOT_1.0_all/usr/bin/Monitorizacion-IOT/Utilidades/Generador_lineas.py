from datetime import date
from datetime import datetime

'''
Clase que genera las líneas de texto legibles para poder ser procesadas por logstash 

'''
class Generador_lineas:
    def generar_linea(idSensor, date, reading):

        line = "{\"sensorId\":\"" + str(idSensor) + "\",\"datetime\":\"" + date.strftime("%d/%m/%Y %H:%M:%S") + "\""
        line += ",\"reading\":{"

        firstReading = True

        for campo in reading.items():
            if(firstReading == False):
                line += ","

            line += "\"" + campo[0] + "\":"+ str(campo[1]) +""
            firstReading = False

        line += "}}"

        return line
