import pickle
import re

import os
import sys

PATH=os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))


from Prediccion.Modelo import * 


class Persistencia_modelo():

    @staticmethod
    def guardar(modelo):

        with open(modelo.nombre,"wb") as file:
            pickle.dump(modelo.model, file)

    @staticmethod
    def cargar(nombreModelo):
        
        tipoModelo = re.sub("model","",nombreModelo).split("_")[0]
        idSensor = re.sub(".pickle","",nombreModelo).split("_")[1]
        model = None
        modelo = None
        
        try:
            with open(PATH + "/modelos/" + nombreModelo , "rb") as file:
                model = pickle.load(file)
            
            if(tipoModelo == "Detretor"):
                modelo = Modelo_Detrender(idSensor)

            if(tipoModelo == "SNARIMAX"):
                modelo = Modelo_SNARIMAX(idSensor)

            modelo.cargar(model)

        except Exception as e:
            raise Exception

        return modelo
