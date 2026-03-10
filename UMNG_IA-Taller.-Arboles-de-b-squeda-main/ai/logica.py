from collections import deque #Para el árbol de búsqueda base
import heapq #Para la cola de prioridad de Mejor Primero. Funciona como una lista que se puede reordenar automaticamente
from abc import ABC, abstractmethod #Para definir clase abstracta

# --- CLASE NODO: REPRESENTA UN PUNTO EN EL ÁRBOL ---
class Nodo:
    def __init__(self, estado, padre=None, accion=None, costo=0, heuristica=0):
        self.estado = estado    #Coordenada (fila, col)
        self.padre = padre      #Referencia al Nodo papá (conecta el árbol)
        self.accion = accion    #Dirección tomada
        self.costo = costo      #Profundidad en el árbol
        self.heuristica = heuristica #h(n): estimación a la meta
        self.f = costo + heuristica  #f(n) = g(n) + h(n)

    #Comparador para la cola de prioridad (heapq)
    def __lt__(self, otro):
        return self.f < otro.f #Simplemente compara los costos entre 2 nodos

    def __repr__(self): #Método de representación, como se muestra en consola
        return f"{self.estado}" #Le dice a la consola que muestre el estado propio del nodo

# --- CLASE MOLDE (ABSTRACTA) ---
class MotorBusqueda(ABC): #Abstracta
    def __init__(self, tamano_tablero=5): #Solamente define el tamaño del tablero
        self.tamano = tamano_tablero

    @abstractmethod
    def obtener_frontera(self): #Método abstracto que sobreescribira cada clase que herede de esta, en este momento, no hace nada
        pass

    def buscar(self, inicio, meta): #Arbol de busqueda general, común en la mayoría de algoritmos (Amplitud, Profundidad) y base para los demás
        #Nodo raíz
        nodo_raiz = Nodo(inicio)
        
        #Frontera (depende del algoritmo)
        frontera = self.obtener_frontera()
        frontera.append(nodo_raiz) #Lista que va apilando cada nodo
        
        #Registro de lo que ya se visito
        visitados = set() #set() es una lista con esteroides, o llamado conjunto, ya que no permitirá nunca duplicados entre sus objetos
        paso = 0

        while frontera:
            #Se extrae un nodo de la fronte
            nodo_actual = self.extraer_de_frontera(frontera)

            #Verifica si es el objetivo
            if nodo_actual.estado == meta:
                return self.reconstruir_camino(nodo_actual)

            #Expansión del nodo, verifica primero si ya se visitó
            if nodo_actual.estado not in visitados:
                visitados.add(nodo_actual.estado) #Se añade al conjunto de visitados
                paso += 1
                
                #Método de expansión: obtener vecinos
                for vecino_estado, accion in self.obtener_vecinos(nodo_actual.estado):
                    if vecino_estado not in visitados:
                        #Se crea el hijo, y luego se añade a la frontera
                        hijo = Nodo(vecino_estado, nodo_actual, accion, nodo_actual.costo + 1)
                        frontera.append(hijo)
                
                #Información general del algoritmo para conocer su mente paso por paso
                print(f"{paso:<5} | {str(nodo_actual.estado):<10} | {str(nodo_actual.accion):<10} | {list(frontera)}")

        return [] #Manejo común en el tipo de datos para evitar errores del tipo NoneType, toda función siempre trabajará con una lista así esté vacía (El equivalente a error en este caso)

    @abstractmethod
    def extraer_de_frontera(self, frontera): #Igual que con obtener frontera, depende del tipo de búsqueda por lo que se sobreeescribe en cada clase hija
        pass

    def obtener_vecinos(self, pos): #Función de ojos para PacMan, le permite ver sus alrededores a traves de las casillas ortogonalmente vecinas
        f, c = pos #Fila y columna trabajan con la posicion del nodo actual
        movimientos = {"arriba": (f-1, c), "abajo": (f+1, c), "derecha": (f, c+1), "izquierda": (f, c-1)} #Movimientos legales
        validos = [] #Lista de los vecinos legales
        for act, n_pos in movimientos.items(): #Verifica cada uno de los items dentro de movimientos (Cada una de las direcciones posibles)
            if 1 <= n_pos[0] <= self.tamano and 1 <= n_pos[1] <= self.tamano: #Verifica legalidad de cada posicion en el tablero de acuerdo a las reglas
                validos.append((n_pos, act)) #Agrega los vecinos validos unicamente
        return validos #Retorna la lista con los vecinos validos

    def reconstruir_camino(self, nodo_final): #Funcion memoria de PacMAn
        """Camina desde la meta hacia el inicio usando los enlaces 'padre'"""
        camino = [] #Lista vacia que almacenara el camino que recorrio pacman hasta llegar a la salida
        actual = nodo_final #Meta, inicia ahi
        while actual is not None: #Revisa cada uno de los nodos y sus padres para encontrar el camino de vuelta al inicio
            camino.append(actual.estado)
            actual = actual.padre
        return camino[::-1] # Lo volteo para que sea Inicio -> Meta. Escencial para la animacion en la GUI

# --- IMPLEMENTACIÓN DE AMPLITUD ---
class BusquedaAmplitud(MotorBusqueda): #Hereda de la clase abstracta MotorBusqueda
    def obtener_frontera(self): #Sobreescritura del metodo de la clase abstracta
        return deque() #Lista de doble salida en las puntas (izquierda - derecha, permite acceso por ambos lados) mas eficiente que las listas comunes de python
    
    def extraer_de_frontera(self, frontera): #Sobreescritura del metodo de la clase abstracta
        return frontera.popleft() # Comportamiento FIFO (Cola), gracias al popleft que accede al primer nodo en entrar a la lista

# --- IMPLEMENTACIÓN DE MEJOR PRIMERO ---
class BusquedaMejorPrimero(MotorBusqueda): #Hereda de la clase abstracta MotorBusqueda
    def obtener_frontera(self): #Sobreescritura del metodo de la clase abstracta
        return [] # Se usa como lista para heapq, no se usa deque como en los demas porque no es compatible con heapq, se necesita una lista que permita alterarse de cualquier manera, incluso accediendo primero a elementos intermedios

    def extraer_de_frontera(self, frontera):
        # POP(frontera) devuelve el nodo con menor f(n)
        return heapq.heappop(frontera) #Es el nodo .pop() propio de la libreria, toma en cuenta nodos intermedios y saca el que haya resultado beneficioso en la comparacion con f(n)

    def calcular_heuristica(self, actual, meta): #Se utiliza este método como formula h(n) debido a su simplicidad técnica
        """Distancia de Manhattan: |x1-x2| + |y1-y2|"""
        return abs(actual[0] - meta[0]) + abs(actual[1] - meta[1])

    def buscar(self, inicio, meta): #Sobreescritura del método de busqueda, debido a que su árbol es distinto al base
        """
        Implementación de Búsqueda Mejor Primero.
        Prioriza nodos según f(n) = g(n) + h(n)
        """
        # 1. Nodo inicial con su h(n)
        h_inicial = self.calcular_heuristica(inicio, meta)
        nodo_raiz = Nodo(inicio, costo=0, heuristica=h_inicial)
        
        # 2. Inicializar frontera como cola de prioridad
        frontera = self.obtener_frontera()
        heapq.heappush(frontera, nodo_raiz) #Es un append que realiza comparaciones internas para reorganizarse de acuerdo al menor valor en el h(n) de cada nodo
        
        # 3. Visitados guarda el costo mínimo para llegar a un estado
        visitados = {} #Se usa un diccionario porque en este caso especifico, al algoritmo le importa tanto el estado del nodo, como su valor. Ademas que permite revisitar y reevaluar nodos
        paso = 0

        print(f"\n--- INICIANDO BÚSQUEDA MEJOR PRIMERO ---")

        while frontera:
            # Extraer el nodo con f(n) mínimo
            nodo_actual = self.extraer_de_frontera(frontera)

            if nodo_actual.estado == meta: #Verifica si llego a la meta
                print(f"¡META! Pasos: {paso}, Costo final: {nodo_actual.costo}")
                return self.reconstruir_camino(nodo_actual)

            # Si ya se visito este punto con un costo menor, no se expande de nuevo
            if nodo_actual.estado in visitados and visitados[nodo_actual.estado] <= nodo_actual.costo:
                continue

            visitados[nodo_actual.estado] = nodo_actual.costo #Añadir a diccionario
            paso += 1

            # 4. Expandir vecinos
            for vecino_estado, accion in self.obtener_vecinos(nodo_actual.estado):
                g_hijo = nodo_actual.costo + 1 # Costo de paso = 1
                
                if vecino_estado not in visitados or g_hijo < visitados[vecino_estado]: #Verifica tanto disponibilidad como costo del nodo a revisar
                    h_hijo = self.calcular_heuristica(vecino_estado, meta) #Verifica costo
                    hijo = Nodo(vecino_estado, nodo_actual, accion, g_hijo, h_hijo)
                    heapq.heappush(frontera, hijo) #Reordena la lista para evaluar los mejores costes siempre
            
            # Debug para la tabla de la profe
            print(f"Paso {paso:<2} | Nodo: {str(nodo_actual.estado):<10} | f: {nodo_actual.f:<2} (g:{nodo_actual.costo} + h:{nodo_actual.heuristica})")

        return [] #Retorno comun de listas entre las funciones

# --- IMPLEMENTACIÓN DE PROFUNDIDAD PRIMERO ---
class BusquedaProfundidadPrimero(MotorBusqueda): #Hereda de clase abstracta
    def obtener_frontera(self): #Igual que en amplitud, por la versatilidad de este tipo de lista
        return deque()
    
    def extraer_de_frontera(self, frontera):
        return frontera.pop() # Comportamiento FIFO (Cola), gracias al .pop()

# --- IMPLEMENTACIÓN DE PROFUNDIDAD LIMITADA ---
class BusquedaProfundidadLimitada(BusquedaProfundidadPrimero):
    def buscar(self, inicio, meta, limite=100, limite_profundidad=None): #Reescritura del método buscar, tiene ligeras variaciones respecto al base, la mas importante es que recibe un atributo extra en forma de profundidad maxima
        """
        Búsqueda limitada. 
        - limite: Límite de pasos/nodos expandidos (para la acción de UI).
        - limite_profundidad: Límite de nivel en el árbol (para la Iterativa).
        """
        nodo_raiz = Nodo(inicio) #Verificacion nodal igual que en el algoritmo base
        frontera = self.obtener_frontera()
        frontera.append(nodo_raiz)
        
        resultado_estado = "fallo" #Variable nueva, necesaria para la busqueda iterativa
        pasos_expandidos = 0

        print(f"\n--- DLS: Iniciando con límite de nodos: {limite} ---")

        while frontera:
            # Control por cantidad de pasos expandidos (Solicitado por el usuario)
            if pasos_expandidos >= limite:
                print(f"Alcanzado límite de expansión de {limite} nodos.")
                break

            nodo_actual = self.extraer_de_frontera(frontera) #Expansión de un nodo

            if nodo_actual.estado == meta: #Verifica si es la meta
                return self.reconstruir_camino(nodo_actual), "solucion"

            # Control por profundidad (Requerido para Profundidad Iterativa)
            if limite_profundidad is not None and nodo_actual.costo >= limite_profundidad: #Solamente si llego a la profundidad limite sin encontrar nada
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

        # Si se sale del bucle y no es solución, devolvemos el estado acumulado
        return [], resultado_estado #Es el único algoritmo que se sale de responder únicamente con la lsita, porque la BPI necesita este segundo argumento de resultado

# --- IMPLEMENTACIÓN DE PROFUNDIDAD LIMITADA ---
class BusquedaProfundidadIterativa(MotorBusqueda):
    def __init__(self, tamano_tablero=5):
        super().__init__(tamano_tablero) #Hereda la propiedad de la clase abstracta
        self.motor_limitado = BusquedaProfundidadLimitada(tamano_tablero) #Añade esta propiedad que simplemente llama a la BPL

    def obtener_frontera(self): return None #No usa frontera propia
    def extraer_de_frontera(self, f): return None #No usa frontera propia, no extrae

    def buscar(self, inicio, meta): #Reescritura del método a partir del pseudocódigo
        """
        Llama repetidamente a DLS incrementando el límite de profundidad.
        """
        print(f"\n--- INICIANDO BÚSQUEDA PROFUNDIDAD ITERATIVA ---")
        
        # El límite de pasos expandidos en IDS suele ser muy alto o inexistente 
        # para dejar que la profundidad controle el corte.
        for d in range(100): 
            print(f"\nProbando profundidad nivel: {d}")
            
            # Aquí se llama a la BPL pasando el nivel como limite_profundidad
            ruta, estado = self.motor_limitado.buscar(inicio, meta, limite=1000, limite_profundidad=d)
            
            if estado != "corte": #Como en el pseudocogido, usa el recurso extra del argloritmo de BPL para decidir como continuar en la busqueda
                if estado == "solucion":
                    print(f"¡Solución encontrada en profundidad {d}!")
                    return ruta
                else:
                    print("No existe solución en el espacio de estados.")
                    return []
        
        return [] #Vuelve a retornar lista como los demas
