import heapq
import json
import os


class GrafoStarWars:


    def __init__(self):
        self.vertices = {}  
        self.episodios_totales = {}  

    def agregar_vertice(self, personaje, total_eps=0):
        if personaje not in self.vertices:
            self.vertices[personaje] = {}
            self.episodios_totales[personaje] = total_eps

    def agregar_arista(self, p1, p2, episodios_juntos):
        """Agrega una arista no dirigida con el número de episodios que comparten."""
        self.agregar_vertice(p1)
        self.agregar_vertice(p2)
        self.vertices[p1][p2] = episodios_juntos
        self.vertices[p2][p1] = episodios_juntos

    def mst_prim(self, inicio):
        """
        Algoritmo de Prim para obtener el Árbol de Expansión Mínimo (MST)
        comenzando desde el vértice 'inicio'.
        """
        if inicio not in self.vertices:
            return [], 0

        visitados = set[inicio]
        aristas_mst = []
        peso_total = 0
        heap = []

        for vecino, peso in self.vertices[inicio].items():
            heapq.heappush(heap, (peso, inicio, vecino))

        while heap and len(visitados) < len(self.vertices):
            peso, u, v = heapq.heappop(heap)
            if v not in visitados:
                visitados.add(v)
                aristas_mst.append((u, v, peso))
                peso_total += peso

                for vecino, p in self.vertices[v].items():
                    if vecino not in visitados:
                        heapq.heappush(heap, (p, v, vecino))

        return aristas_mst, peso_total

    def maximo_episodios_compartidos(self):
        """Calcula el número máximo de episodios compartidos y los pares coincidentes."""
        max_peso = -1
        pares_max = []
        visitados = set()

        for u in self.vertices:
            for v, peso in self.vertices[u].items():
                par = tuple(sorted([u, v]))
                if par not in visitados:
                    visitados.add(par)
                    if peso > max_peso:
                        max_peso = peso
                        pares_max = [par]
                    elif peso == max_peso:
                        pares_max.append(par)

        return max_peso, pares_max

    def dijkstra_camino_corto(self, origen, destino):
        """
        Calcula el camino más corto entre dos personajes utilizando el algoritmo de Dijkstra.
        """
        if origen not in self.vertices or destino not in self.vertices:
            return None, float('inf')

        distancias = {v: float('inf') for v in self.vertices}
        predecesores = {v: None for v in self.vertices}
        distancias[origen] = 0
        pq = [(0, origen)]

        while pq:
            dist_actual, u = heapq.heappop(pq)

            if u == destino:
                break

            if dist_actual > distancias[u]:
                continue

            for vecino, peso in self.vertices[u].items():
                nueva_dist = dist_actual + peso
                if nueva_dist < distancias[vecino]:
                    distancias[vecino] = nueva_dist
                    predecesores[vecino] = u
                    heapq.heappush(pq, (nueva_dist, vecino))

        camino = []
        actual = destino
        if distancias[destino] == float('inf'):
            return [], float('inf')

        while actual is not None:
            camino.append(actual)
            actual = predecesores[actual]

        camino.reverse()
        return camino, distancias[destino]

    def personajes_en_nueve_episodios(self):
        """Determina los personajes que aparecieron en los 9 episodios de la saga."""
        resultado = []
        for p, eps in self.episodios_totales.items():
            if eps == 9:
                resultado.append(p)
            else:
                for peso in self.vertices[p].values():
                    if peso == 9 and p not in resultado:
                        resultado.append(p)
        return sorted(resultado)

def crear_personajes_json_base():
    """Genera el archivo personajes.json con la estructura y claves actualizadas."""
    datos = {
      "personajes": [
        {"nombre": "Luke Skywalker", "apariciones_totales": 6},
        {"nombre": "Darth Vader", "apariciones_totales": 6},
        {"nombre": "Yoda", "apariciones_totales": 6},
        {"nombre": "Boba Fett", "apariciones_totales": 3},
        {"nombre": "C-3PO", "apariciones_totales": 9},
        {"nombre": "Leia", "apariciones_totales": 6},
        {"nombre": "Rey", "apariciones_totales": 3},
        {"nombre": "Kylo Ren", "apariciones_totales": 3},
        {"nombre": "Chewbacca", "apariciones_totales": 7},
        {"nombre": "Han Solo", "apariciones_totales": 5},
        {"nombre": "R2-D2", "apariciones_totales": 9},
        {"nombre": "BB-8", "apariciones_totales": 3}
      ],
      "aristas": [
        {"origen": "C-3PO", "destino": "R2-D2", "episodios_juntos": 9},
        {"origen": "Luke Skywalker", "destino": "Leia", "episodios_juntos": 4},
        {"origen": "Luke Skywalker", "destino": "Han Solo", "episodios_juntos": 3},
        {"origen": "Luke Skywalker", "destino": "Darth Vader", "episodios_juntos": 3},
        {"origen": "Luke Skywalker", "destino": "Yoda", "episodios_juntos": 3},
        {"origen": "Leia", "destino": "Han Solo", "episodios_juntos": 4},
        {"origen": "Leia", "destino": "C-3PO", "episodios_juntos": 6},
        {"origen": "Han Solo", "destino": "Chewbacca", "episodios_juntos": 5},
        {"origen": "Chewbacca", "destino": "Rey", "episodios_juntos": 3},
        {"origen": "Rey", "destino": "Kylo Ren", "episodios_juntos": 3},
        {"origen": "Rey", "destino": "BB-8", "episodios_juntos": 3},
        {"origen": "BB-8", "destino": "R2-D2", "episodios_juntos": 3},
        {"origen": "Yoda", "destino": "Darth Vader", "episodios_juntos": 1},
        {"origen": "Darth Vader", "destino": "Boba Fett", "episodios_juntos": 2},
        {"origen": "Boba Fett", "destino": "Han Solo", "episodios_juntos": 2}
      ]
    }

    with open("personajes.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def main():
    if not os.path.exists("personajes.json"):
        crear_personajes_json_base()

    grafo = GrafoStarWars()

    with open("personajes.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Actualización de claves de acceso al JSON: "apariciones_totales"
    for p in data.get("personajes", []):
        grafo.agregar_vertice(p["nombre"], p.get("apariciones_totales", 0))

    # Actualización de claves de acceso al JSON: "aristas", "origen", "destino"
    for r in data.get("aristas", []):
        grafo.agregar_arista(r["origen"], r["destino"], r["episodios_juntos"])

    print("==================================================")
    print("      GRAFO STAR WARS - RESOLUCIÓN TAREAS       ")
    print("==================================================\n")

    print("--- 1. ÁRBOLES DE EXPANSIÓN MÍNIMO (PRIM) ---")
    for inicio in ["C-3PO", "Yoda", "Leia"]:
        mst, peso = grafo.mst_prim(inicio)
        print(f"\n[MST desde '{inicio}'] Peso Acumulado: {peso}")
        print("Aristas:")
        for u, v, w in mst:
            print(f"  ({u}) <--- {w} epis. ---> ({v})")

    print("\n--------------------------------------------------")
    print("--- 2. MÁXIMO DE EPISODIOS COMPARTIDOS ---")
    max_ep, pares = grafo.maximo_episodios_compartidos()
    print(f"Número máximo de episodios compartidos: {max_ep}")
    print("Pares coincidentes:")
    for p1, p2 in pares:
        print(f"  • {p1} y {p2}")

    print("\n--------------------------------------------------")
    print("--- 3. CAMINOS MÁS CORTOS (DIJKSTRA) ---")
    c1, d1 = grafo.dijkstra_camino_corto("C-3PO", "R2-D2")
    print("• De C-3PO a R2-D2:")
    print(f"  Camino: {' -> '.join(c1)} (Costo: {d1})")

    c2, d2 = grafo.dijkstra_camino_corto("Yoda", "Darth Vader")
    print("\n• De Yoda a Darth Vader:")
    print(f"  Camino: {' -> '.join(c2)} (Costo: {d2})")

    print("\n--------------------------------------------------")
    print("--- 4. PERSONAJES PRESENTES EN LOS 9 EPISODIOS ---")
    p9 = grafo.personajes_en_nueve_episodios()
    print(f"Personajes presentes en los 9 episodios: {', '.join(p9)}")
    print("==================================================")

if __name__ == "__main__":
    main()