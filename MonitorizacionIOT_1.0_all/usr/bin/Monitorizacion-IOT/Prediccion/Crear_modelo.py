from Modelo import *
from Persistencia_modelo import *

import sys
'''
Ejecutando este fichero con python se podrá crear un nuevo modelo 
para un sensor

se ha de inicializar el modelo que se desee para el sensor junto a los
parámetros necesarios.
'''
if __name__ == "__main__":

    idSensor = 4051

    #modelo = Modelo_Detrender(idSensor)
    #modelo.inicializar(window=0,intercept_lr=0,sgd=0)

    modelo = Modelo_SNARIMAX(idSensor)
    modelo.inicializar(q=2,m=30,sp=6,sq=10,intercept_init=12,sgd=0.01, intercerpt_lr=0.3)

    Persistencia_modelo.guardar(modelo)
