from collections import deque # Importamos la cola para la búsqueda en amplitud
import heapq # Para la cola de prioridad de Mejor Primero
from abc import ABC, abstractmethod # Para definir nuestra clase molde

# --- CLASE NODO: REPRESENTA UN PUNTO EN EL ÁRBOL ---
class Nodo:
    def __init__(self, estado, padre=None, accion=None, costo=0, heuristica=0):
        self.estado = estado    # Coordenada (fila, col)
        self.padre = padre      # Referencia al Nodo papá (conecta el árbol)
        self.accion = accion    # Dirección tomada
        self.costo = costo      # Profundidad en el árbol
        self.heuristica = heuristica # h(n): estimación a la meta
        self.f = costo + heuristica  # f(n) = g(n) + h(n)

    # Comparador para la cola de prioridad (heapq)
    def __lt__(self, otro):
        return self.f < otro.f

    def __repr__(self):
        return f"{self.estado}"

# --- CLASE MOLDE (ABSTRACTA) ---
class MotorBusqueda(ABC):
    def __init__(self, tamano_tablero=5):
        self.tamano = tamano_tablero

    @abstractmethod
    def obtener_frontera(self):
        pass

    def buscar(self, inicio, meta): #Arbol de busqueda general
        # 1. Nodo raíz
        nodo_raiz = Nodo(inicio)
        
        # 2. Frontera (depende del algoritmo)
        frontera = self.obtener_frontera()
        frontera.append(nodo_raiz)
        
        # 3. Registro de lo que ya vimos
        visitados = set()
        paso = 0

        while frontera:
            # Extraemos un nodo de la frontera
            nodo_actual = self.extraer_de_frontera(frontera)

            # ¿Llegamos al objetivo?
            if nodo_actual.estado == meta:
                return self.reconstruir_camino(nodo_actual)

            # Expansión del nodo
            if nodo_actual.estado not in visitados:
                visitados.add(nodo_actual.estado)
                paso += 1
                
                # Método de expansión: obtener vecinos
                for vecino_estado, accion in self.obtener_vecinos(nodo_actual.estado):
                    if vecino_estado not in visitados:
                        # Creamos el nodo hijo en el árbol
                        hijo = Nodo(vecino_estado, nodo_actual, accion, nodo_actual.costo + 1)
                        frontera.append(hijo)
                
                # Imprimimos la tabla para la profe
                print(f"{paso:<5} | {str(nodo_actual.estado):<10} | {str(nodo_actual.accion):<10} | {list(frontera)}")

        return []

    @abstractmethod
    def extraer_de_frontera(self, frontera):
        pass

    def obtener_vecinos(self, pos):
        f, c = pos
        movimientos = {"arriba": (f-1, c), "abajo": (f+1, c), "derecha": (f, c+1), "izquierda": (f, c-1)}
        validos = []
        for act, n_pos in movimientos.items():
            if 1 <= n_pos[0] <= self.tamano and 1 <= n_pos[1] <= self.tamano:
                validos.append((n_pos, act))
        return validos

    def reconstruir_camino(self, nodo_final):
        """Camina desde la meta hacia el inicio usando los enlaces 'padre'"""
        camino = []
        actual = nodo_final
        while actual is not None:
            camino.append(actual.estado)
            actual = actual.padre
        return camino[::-1] # Lo volteo para que sea Inicio -> Meta

# --- IMPLEMENTACIÓN DE AMPLITUD ---
class BusquedaAmplitud(MotorBusqueda):
    def obtener_frontera(self):
        return deque()
    
    def extraer_de_frontera(self, frontera):
        return frontera.popleft() # Comportamiento FIFO (Cola)

class BusquedaMejorPrimero(MotorBusqueda):
    def obtener_frontera(self):
        return [] # Se usa como lista para heapq

    def extraer_de_frontera(self, frontera):
        # POP(frontera) devuelve el nodo con menor f(n)
        return heapq.heappop(frontera)

    def calcular_heuristica(self, actual, meta):
        """Distancia de Manhattan: |x1-x2| + |y1-y2|"""
        return abs(actual[0] - meta[0]) + abs(actual[1] - meta[1])

    def buscar(self, inicio, meta):
        """
        Implementación de Búsqueda Mejor Primero.
        Prioriza nodos según f(n) = g(n) + h(n)
        """
        # 1. Nodo inicial con su h(n)
        h_inicial = self.calcular_heuristica(inicio, meta)
        nodo_raiz = Nodo(inicio, costo=0, heuristica=h_inicial)
        
        # 2. Inicializar frontera como cola de prioridad
        frontera = self.obtener_frontera()
        heapq.heappush(frontera, nodo_raiz)
        
        # 3. Visitados guarda el costo mínimo para llegar a un estado
        visitados = {} 
        paso = 0

        print(f"\n--- INICIANDO BÚSQUEDA MEJOR PRIMERO ---")

        while frontera:
            # Extraer el nodo con f(n) mínimo
            nodo_actual = self.extraer_de_frontera(frontera)

            if nodo_actual.estado == meta:
                print(f"¡META! Pasos: {paso}, Costo final: {nodo_actual.costo}")
                return self.reconstruir_camino(nodo_actual)

            # Si ya visitamos este punto con un costo menor, no lo expandimos de nuevo
            if nodo_actual.estado in visitados and visitados[nodo_actual.estado] <= nodo_actual.costo:
                continue

            visitados[nodo_actual.estado] = nodo_actual.costo
            paso += 1

            # 4. Expandir vecinos
            for vecino_estado, accion in self.obtener_vecinos(nodo_actual.estado):
                g_hijo = nodo_actual.costo + 1 # Costo de paso = 1
                
                if vecino_estado not in visitados or g_hijo < visitados[vecino_estado]:
                    h_hijo = self.calcular_heuristica(vecino_estado, meta)
                    hijo = Nodo(vecino_estado, nodo_actual, accion, g_hijo, h_hijo)
                    heapq.heappush(frontera, hijo)
            
            # Debug para la tabla de la profe
            print(f"Paso {paso:<2} | Nodo: {str(nodo_actual.estado):<10} | f: {nodo_actual.f:<2} (g:{nodo_actual.costo} + h:{nodo_actual.heuristica})")

        return []

class BusquedaProfundidadPrimero(MotorBusqueda):
    def obtener_frontera(self):
        return deque()
    
    def extraer_de_frontera(self, frontera):
        return frontera.pop() # Comportamiento FIFO (Cola)

class BusquedaProfundidadLimitada(BusquedaProfundidadPrimero):
    def buscar(self, inicio, meta, limite=100, limite_profundidad=None):
        """
        Búsqueda limitada. 
        - limite: Límite de pasos/nodos expandidos (para la acción de UI).
        - limite_profundidad: Límite de nivel en el árbol (para la Iterativa).
        """
        nodo_raiz = Nodo(inicio)
        frontera = self.obtener_frontera()
        frontera.append(nodo_raiz)
        
        resultado_estado = "fallo"
        pasos_expandidos = 0

        print(f"\n--- DLS: Iniciando con límite de nodos: {limite} ---")

        while frontera:
            # Control por cantidad de pasos expandidos (Solicitado por el usuario)
            if pasos_expandidos >= limite:
                print(f"Alcanzado límite de expansión de {limite} nodos.")
                break

            nodo_actual = self.extraer_de_frontera(frontera)

            if nodo_actual.estado == meta:
                return self.reconstruir_camino(nodo_actual), "solucion"

            # Control por profundidad (Requerido para Profundidad Iterativa)
            if limite_profundidad is not None and nodo_actual.costo >= limite_profundidad:
                resultado_estado = "corte"
                continue

            pasos_expandidos += 1
            
            # Expansión de árbol (sin visitados globales como en el pseudocódigo)
            vecinos = self.obtener_vecinos(nodo_actual.estado)
            for vecino_estado, accion in reversed(vecinos):
                # Evitar ciclo inmediato con el padre para no entrar en bucle infinito simple
                if nodo_actual.padre and vecino_estado == nodo_actual.padre.estado:
                    continue
                
                hijo = Nodo(vecino_estado, nodo_actual, accion, nodo_actual.costo + 1)
                frontera.append(hijo)
            
            print(f"Paso {pasos_expandidos:<2} | Nodo: {str(nodo_actual.estado):<10} | Prof: {nodo_actual.costo:<2}")

        # Si salimos del bucle y no es solución, devolvemos el estado acumulado
        return [], resultado_estado

class BusquedaProfundidadIterativa(MotorBusqueda):
    def __init__(self, tamano_tablero=5):
        super().__init__(tamano_tablero)
        self.motor_limitado = BusquedaProfundidadLimitada(tamano_tablero)

    def obtener_frontera(self): return None # No usa frontera propia
    def extraer_de_frontera(self, f): return None

    def buscar(self, inicio, meta):
        """
        Llama repetidamente a DLS incrementando el límite de profundidad.
        """
        print(f"\n--- INICIANDO BÚSQUEDA PROFUNDIDAD ITERATIVA ---")
        
        # El límite de pasos expandidos en IDS suele ser muy alto o inexistente 
        # para dejar que la profundidad controle el corte.
        for d in range(100): 
            print(f"\nProbando profundidad nivel: {d}")
            
            # Aquí llamamos a la limitada pasando el nivel como limite_profundidad
            ruta, estado = self.motor_limitado.buscar(inicio, meta, limite=1000, limite_profundidad=d)
            
            if estado != "corte":
                if estado == "solucion":
                    print(f"¡Solución encontrada en profundidad {d}!")
                    return ruta
                else:
                    print("No existe solución en el espacio de estados.")
                    return []
        
        return []