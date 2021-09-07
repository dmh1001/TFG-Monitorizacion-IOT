import pickle
from Modelo import *

class Persistencia_modelo():

    def cargar(nombre):
        try:
            with open(nombre , "rb") as file:
                return pickle.load(file)

        except Exception as e:
            raise Exception

    def guardar(modelo):

        with open(modelo.nombre,"wb") as file:
            pickle.dump(modelo.modelo, file)


