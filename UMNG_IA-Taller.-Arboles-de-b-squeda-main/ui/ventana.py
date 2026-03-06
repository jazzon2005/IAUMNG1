import tkinter as tk
from game.tablero import Tablero

class Ventana:
    def __init__(self, root):
        self.root = root
        self.root.title("Pacman IA - Búsqueda Modular")
        
        # Configuración de dimensiones
        self.tamano_celda = 80
        self.tamano_tablero = 5
        self.canvas_dim = self.tamano_celda * self.tamano_tablero
        
        # UI Elements
        self.canvas = tk.Canvas(root, width=self.canvas_dim, height=self.canvas_dim, bg="white")
        self.canvas.pack(pady=10, padx=20)
        
        # Diccionario de botones para evitar repetición
        # Formato: "Texto del botón": "nombre_metodo_en_tablero"
        botones = {
            "Amplitud": "obtener_ruta_amplitud",
            "Mejor Primero": "obtener_ruta_mejorPrimero",
            "Profundidad": "obtener_ruta_profundidad",
            "Profundidad Limitada": "obtener_ruta_profundidadLim",
            "Profundidad Iterativa": "obtener_ruta_profundidadIt"
        }

        # Crear botones dinámicamente
        for texto, metodo in botones.items():
            btn = tk.Button(
                root, 
                text=f"Calcular Ruta {texto}", 
                width=30,
                command=lambda m=metodo: self.ejecutar_busqueda(m)
            )
            btn.pack(pady=2)
        
        self.pacman_id = None
        self.ruta = []
        self.paso_actual = 0
        self.dibujar_tablero()

    def dibujar_tablero(self):
        """Dibuja la cuadrícula del mapa."""
        for f in range(self.tamano_tablero):
            for c in range(self.tamano_tablero):
                x1, y1 = c * self.tamano_celda, f * self.tamano_celda
                self.canvas.create_rectangle(
                    x1, y1, x1 + self.tamano_celda, y1 + self.tamano_celda, 
                    fill="#1d1d1d", outline="blue"
                )

    def dibujar_pacman(self, pos):
        """Actualiza la posición del círculo amarillo."""
        if self.pacman_id: 
            self.canvas.delete(self.pacman_id)
        
        # Ajuste de coordenadas (Tablero 1-5 a Pixeles)
        y = (pos[0] - 1) * self.tamano_celda + (self.tamano_celda // 2)
        x = (pos[1] - 1) * self.tamano_celda + (self.tamano_celda // 2)
        
        r = 25 # Radio de Pacman
        self.pacman_id = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="yellow", outline="black")

    def ejecutar_busqueda(self, nombre_metodo):
        """Método genérico para ejecutar cualquier algoritmo de búsqueda."""
        t = Tablero(self.tamano_tablero)
        metodo = getattr(t, nombre_metodo)
        resultado = metodo()
        
        # Manejo de desempaquetado para Profundidad Limitada (que devuelve tupla)
        if isinstance(resultado, tuple):
            self.ruta = resultado[0]
        else:
            self.ruta = resultado

        if self.ruta:
            self.paso_actual = 0
            self.animar()
        else:
            print(f"No se encontró ruta con el método: {nombre_metodo}")

    def animar(self):
        """Ciclo de animación basado en el after de Tkinter."""
        if self.paso_actual < len(self.ruta):
            self.dibujar_pacman(self.ruta[self.paso_actual])
            self.paso_actual += 1
            self.root.after(400, self.animar)