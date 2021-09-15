import json
from .Generador_lineas import *

class Tratamiento_sensor_data:

    def transformarJSON(self, fichero, idSensor):
        linea = []
        for line in fichero['histdata']:
            if(line['Valor'] != ''):
                date = datetime.strptime(line.pop('datetime'), '%d/%m/%Y %H:%M:%S')

                try:
                    line.pop('coverage')
                except:
                    pass

                linea.append(Generador_lineas.generar_linea(idSensor,date,line))

        return linea


    def leerJSON(self, ruta):
        with open(ruta,"rb") as file:
            data = json.load(file)
            return data
