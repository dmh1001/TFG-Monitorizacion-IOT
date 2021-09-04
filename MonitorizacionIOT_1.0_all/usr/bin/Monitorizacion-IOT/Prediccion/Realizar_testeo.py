import sys
from Testeo import *
import os

PATH = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))


if __name__ == "__main__":

    idSensor = sys.argv[1]
    fecha_inicio = sys.argv[2]
    fecha_final = sys.argv[3]

    print(fecha_inicio)

    tester = Testeo(idSensor)

    rmse = tester.metrica_RMSE(fecha_inicio, fecha_final)
    mae = tester.metrica_MAE(fecha_inicio, fecha_final)
    mse = tester.metrica_MSE(fecha_inicio, fecha_final)
    r2 = tester.metrica_R2(fecha_inicio, fecha_final)

    with open(PATH + '/ResultadosTest/testeo.txt', "a") as file:
        file.write(str(fecha_inicio) + " - " + str(fecha_final) + " RMSE: " + str(rmse) + " MAR: " + str(mae) + " MSE: " + str(mse) + " R2: " + str(r2) )
