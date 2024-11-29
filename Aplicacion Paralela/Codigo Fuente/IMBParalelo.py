import math
import random
import time
from multiprocessing import Pool

def generar_nodos_random(cantidad):
    nodos = []
    for _ in range(cantidad):
        x = random.randint(1, 10000)
        y = random.randint(1, 10000)
        nodos.append((x, y))
    return nodos

def escribir_archivo(nombre_archivo, nodos):
    with open(nombre_archivo, 'w') as archivo:
        archivo.write("NODE_COORD_SECTION\n")
        for i, (x, y) in enumerate(nodos, start=1):
            archivo.write(f"{i} {x} {y}\n")
        archivo.write("EOF\n")

def distancia_euclidiana(nodo1, nodo2):
    x1, y1 = nodo1
    x2, y2 = nodo2
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia

def calcular_distancias(i, nodos):
    return [distancia_euclidiana(nodos[i], nodos[j]) for j in range(len(nodos))]

def calcular_matriz_distancias_paralelo(nodos):
    with Pool() as pool:
        matriz = pool.starmap(calcular_distancias, [(i, nodos) for i in range(len(nodos))])
    return matriz

def encontrar_arco_menor_costo(matriz):
    min_costo = float('inf')
    i_min, j_min = 0, 0
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] < min_costo:
                min_costo = matriz[i][j]
                i_min, j_min = i, j
    return i_min, j_min

def tsp(matriz_distancias):
    n = len(matriz_distancias)
    nodo_inicial, siguiente_nodo = encontrar_arco_menor_costo(matriz_distancias)
    tour = [nodo_inicial, siguiente_nodo]
    visitados = {nodo_inicial, siguiente_nodo}
    costo_total = 2 * matriz_distancias[nodo_inicial][siguiente_nodo]

    while len(visitados) < n:
        mejor_insercion = None
        menor_incremento = float('inf')
        mejor_k = None
        for k in range(n):
            if k not in visitados:
                for i in range(len(tour) - 1):
                    nodo_i = tour[i]
                    nodo_j = tour[i + 1]
                    costo_insercion = matriz_distancias[nodo_i][k] + matriz_distancias[k][nodo_j] - matriz_distancias[nodo_i][nodo_j]
                    if costo_insercion < menor_incremento:
                        menor_incremento = costo_insercion
                        mejor_insercion = i + 1
                        mejor_k = k
        tour.insert(mejor_insercion, mejor_k)
        visitados.add(mejor_k)
        costo_total += menor_incremento

    if tour[-1] != nodo_inicial:
        tour.append(nodo_inicial)

    tour = [x + 1 for x in tour]
    return tour, costo_total

def leer_archivo(nombre_archivo):
    nodos = []
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
        coordenadas = False
        for linea in lineas:
            if "NODE_COORD_SECTION" in linea:
                coordenadas = True
                continue
            elif "EOF" in linea:
                break
            if coordenadas:
                valores = linea.split()
                x, y = float(valores[1]), float(valores[2])
                nodos.append((x, y))
    return nodos

def main(nombre_archivo):
    inicio = time.time()
    nodos = generar_nodos_random(750)
    escribir_archivo(nombre_archivo, nodos)
    nodos = leer_archivo(nombre_archivo)
    matriz_distancias = calcular_matriz_distancias_paralelo(nodos)
    tour, costo_total = tsp(matriz_distancias)
    print("Tour TSP:", tour)
    print("Costo total del tour:", costo_total)
    fin = time.time()
    print("Tiempo de ejecución:", fin - inicio, "segundos")

if __name__ == "__main__":
    nombre_archivo = "nodos.txt"
    main(nombre_archivo)
