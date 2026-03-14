import tkinter as tk
from game.tablero import Tablero

class Ventana:
    def __init__(self, root):
        self.root = root #Inicializacion logica clasica de la GUI
        self.root.title("Pacman IA - Explorador de Algoritmos")
        self.root.configure(bg="#121212") # Fondo oscuro
        
        # --- CONFIGURACIÓN ---
        self.tamano_celda = 70
        self.tamano_tablero = 5
        self.canvas_dim = self.tamano_celda * self.tamano_tablero
        
        #Coordenadas fijas para visualización de elementos importantes
        self.inicio_pos = (5, 1)
        self.meta_pos = (1, 5)
        
        # --- ESTRUCTURA DE LA INTERFAZ (GRID) ---
        #Panel Izquierdo: Canvas
        self.canvas = tk.Canvas(root, width=self.canvas_dim, height=self.canvas_dim, 
                               bg="#000", highlightthickness=2, highlightbackground="blue")
        self.canvas.grid(row=0, column=0, padx=20, pady=20, rowspan=2)
        
        #Panel Derecho: Controles
        self.frame_controles = tk.Frame(root, bg="#121212")
        self.frame_controles.grid(row=0, column=1, padx=20, pady=20, sticky="n")
        
        #Texto
        tk.Label(self.frame_controles, text="ALGORITMOS DE BÚSQUEDA", 
                 fg="white", bg="#121212", font=("Arial", 12, "bold")).pack(pady=(0, 15))

        #Botones modulares pensados como una especie de diccionario
        botones = [
            ("Amplitud (BFS)", "obtener_ruta_amplitud", "#3498db"),
            ("Mejor Primero (A*)", "obtener_ruta_mejorPrimero", "#2ecc71"),
            ("Profundidad (DFS)", "obtener_ruta_profundidad", "#e74c3c"),
            ("Prof. Limitada", "obtener_ruta_profundidadLim", "#f1c40f"),
            ("Prof. Iterativa", "obtener_ruta_profundidadIt", "#9b59b6")
        ]

        #Instanciacion de cada uno de los botones definidos antes
        for texto, metodo, color in botones:
            btn = tk.Button(
                self.frame_controles, 
                text=texto, 
                width=25,
                bg=color,
                fg="black" if color == "#f1c40f" else "white",
                font=("Arial", 10, "bold"),
                cursor="hand2",
                command=lambda m=metodo: self.ejecutar_busqueda(m)
            )
            btn.pack(pady=5)

        #Panel Inferior Derecho: Información / Leyenda
        self.lbl_info = tk.Label(self.frame_controles, text="Estado: Esperando...", 
                                fg="#aaaaaa", bg="#121212", font=("Arial", 9, "italic"))
        self.lbl_info.pack(pady=20)
        
        # --- ESTADO DE JUEGO ---
        self.pacman_id = None
        self.meta_id = None
        self.puntos_camino = []
        self.ruta = []
        self.paso_actual = 0
        
        #Inicializacion grafica
        self.dibujar_escenario_base()

    def dibujar_escenario_base(self):
        """Dibuja el tablero, el inicio y la meta permanente."""
        self.canvas.delete("all") #Limpia el escenario
        
        #Cuadrícula
        for f in range(self.tamano_tablero):
            for c in range(self.tamano_tablero):
                x1, y1 = c * self.tamano_celda, f * self.tamano_celda
                self.canvas.create_rectangle(
                    x1, y1, x1 + self.tamano_celda, y1 + self.tamano_celda, 
                    outline="#000033", fill="#050505"
                )

        #Dibujar Meta
        my = (self.meta_pos[0] - 1) * self.tamano_celda + (self.tamano_celda // 2)
        mx = (self.meta_pos[1] - 1) * self.tamano_celda + (self.tamano_celda // 2)
        self.canvas.create_oval(mx-15, my-15, mx+15, my+15, fill="#ff0000", outline="white", width=2)
        self.canvas.create_text(mx, my+25, text="META", fill="white", font=("Arial", 8, "bold"))

        #Dibujar Pacman en inicio
        self.dibujar_pacman(self.inicio_pos)

    def dibujar_pacman(self, pos):
        """Dibuja a Pacman con efecto de 'boca' simple."""
        if self.pacman_id: 
            self.canvas.delete(self.pacman_id) #Limpia si ya existia un pacman de pruebas anteriores
        
        y = (pos[0] - 1) * self.tamano_celda + (self.tamano_celda // 2)
        x = (pos[1] - 1) * self.tamano_celda + (self.tamano_celda // 2)
        
        r = 22
        #Pacman (Arco para simular boca abierta)
        self.pacman_id = self.canvas.create_arc(
            x-r, y-r, x+r, y+r, 
            start=30, extent=300, 
            fill="yellow", outline="black"
        )

    #Funcion para mostrar el camino recorrido por pacman
    def dejar_rastro(self, pos):
        """Deja un pequeño punto en el camino recorrido."""
        y = (pos[0] - 1) * self.tamano_celda + (self.tamano_celda // 2)
        x = (pos[1] - 1) * self.tamano_celda + (self.tamano_celda // 2)
        dot = self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="#ffb8ae")
        self.puntos_camino.append(dot)

    def ejecutar_busqueda(self, nombre_metodo):
        #Limpiar rastro anterior
        for p in self.puntos_camino: self.canvas.delete(p)
        self.puntos_camino = []
        
        t = Tablero(self.tamano_tablero) #Instancia tablero y ejecuta la funcion acorde a la declarada por cada boton
        metodo = getattr(t, nombre_metodo)
        resultado = metodo()
        
        if isinstance(resultado, tuple): #Para el caso especial de la profundidad limitada que no solo devuelven una lista
            self.ruta = resultado[0]
        else:
            self.ruta = resultado

        if self.ruta: #Estados para mostrar como esta interactuando el programa en la GUI
            self.lbl_info.config(text=f"Ejecutando: {nombre_metodo}...", fg="#2ecc71")
            self.paso_actual = 0
            self.animar()
        else:
            self.lbl_info.config(text="Error: Sin ruta", fg="#e74c3c")

    def animar(self):
        if self.paso_actual < len(self.ruta):
            pos_actual = self.ruta[self.paso_actual]
            self.dibujar_pacman(pos_actual)
            self.dejar_rastro(pos_actual)
            self.paso_actual += 1
            #Velocidad de animación
            self.root.after(300, self.animar)
        else:
            self.lbl_info.config(text="¡Meta alcanzada!", fg="yellow")
