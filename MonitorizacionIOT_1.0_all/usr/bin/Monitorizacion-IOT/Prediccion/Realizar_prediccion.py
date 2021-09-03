from Modelo import *
import sys

if __name__ == "__main__":
    idSensor = sys.argv[1]
    horizonte = int(sys.argv[2])

    modelo = Modelo_SNARIMAX(idSensor)
    modelo.predecir(horizonte)
