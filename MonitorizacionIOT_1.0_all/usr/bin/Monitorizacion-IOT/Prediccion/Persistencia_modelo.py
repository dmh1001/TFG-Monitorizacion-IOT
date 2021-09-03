import pickle

class Persistencia_modelo():

    def cargar(nombre):
        try:
            with open(nombre , "rb") as file:
                return pickle.load(file)

        except FileNotFoundError as e:
            print("Error, modelo no encontrado")

    def guardar(modelo, nombre):
        with open(nombre,"wb") as file:
            pickle.dump(modelo, file)
