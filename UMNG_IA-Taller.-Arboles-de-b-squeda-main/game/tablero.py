# Importamos los motores de búsqueda desde el archivo de logica
from ai.logica import *

class Tablero:
    """Clase que configura el escenario del juego"""
    def __init__(self, tamano=5):
        self.tamano = tamano
        self.inicio = (5, 1) # Pacman empieza abajo a la izquierda
        self.meta = (1, 5)   # La meta está arriba a la derecha
        
        # Aquí se elige qué "cerebro" usar
        self.motor = None
    
    def obtener_ruta_amplitud(self): 
        self.motor = BusquedaAmplitud(self.tamano)
        """Llama al motor de IA para que resuelva el laberinto"""
        return self.motor.buscar(self.inicio, self.meta)
    
    def obtener_ruta_mejorPrimero(self):
        self.motor = BusquedaMejorPrimero(self.tamano)
        """Llama al motor de IA para que resuelva el laberinto"""
        return self.motor.buscar(self.inicio, self.meta)
    
    def obtener_ruta_profundidad(self):
        self.motor = BusquedaProfundidadPrimero(self.tamano)
        """Llama al motor de IA para que resuelva el laberinto"""
        return self.motor.buscar(self.inicio, self.meta)

    def obtener_ruta_profundidadLim(self):
        self.motor = BusquedaProfundidadLimitada(self.tamano)
        """Llama al motor de IA para que resuelva el laberinto"""
        return self.motor.buscar(self.inicio, self.meta, limite=100)
    
    def obtener_ruta_profundidadIt(self):
        self.motor = BusquedaProfundidadIterativa(self.tamano)
        """Llama al motor de IA para que resuelva el laberinto"""
        return self.motor.buscar(self.inicio, self.meta)
