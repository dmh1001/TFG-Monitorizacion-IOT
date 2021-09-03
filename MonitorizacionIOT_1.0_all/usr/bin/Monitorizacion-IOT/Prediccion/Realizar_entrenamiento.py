import sys
from Modelo import *

if __name__ == "__main__":

    idSensor = sys.argv[1]
    fecha_inicio = sys.argv[2]
    fecha_final = sys.argv[3]

    modelo = Modelo_SNARIMAX(idSensor)
    modelo.entrenar(fecha_inicio, fecha_final)
