from abc import ABC, abstractmethod

class Habitacion(ABC):

    def __init__(self, numero, precio, capacidad, disponible=True):
        self.numero = numero
        self.precio = precio
        self.capacidad = capacidad
        self.disponible = disponible

    @abstractmethod
    def calcular_precio(self):
        """ Calcula el precio de una estadia"""
        pass

    @abstractmethod
    def mostrar_informacion(self):
        """ Muestra información de la habitación"""
        pass

        


