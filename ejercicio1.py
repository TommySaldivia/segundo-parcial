import json


class NodoArbol:
    """Nodo para Árbol Binario de Búsqueda."""
    def __init__(self, clave, dato=None):
        self.clave = clave
        self.datos = [dato] if dato is not None else []
        self.izq = None
        self.der = None

class ArbolBinarioBusqueda:
    """Estructura TDA Árbol Binario de Búsqueda (ABB)."""
    def __init__(self):
        self.raiz = None

    def insertar(self, clave, dato):
        """Inserta un nodo. Si la clave ya existe, acumula en la lista de datos."""
        def _insertar(nodo, clave, dato):
            if nodo is None:
                return NodoArbol(clave, dato)
            if clave == nodo.clave:
                nodo.datos.append(dato)
            elif clave < nodo.clave:
                nodo.izq = _insertar(nodo.izq, clave, dato)
            else:
                nodo.der = _insertar(nodo.der, clave, dato)
            return nodo
        self.raiz = _insertar(self.raiz, clave, dato)

    def buscar_exacto(self, clave):
        """Búsqueda exacta en O(log N)."""
        actual = self.raiz
        while actual:
            if actual.clave == clave:
                return actual.datos
            elif clave < actual.clave:
                actual = actual.izq
            else:
                actual = actual.der
        return []

    def buscar_proximidad(self, subcadena):
        """Búsqueda por subcadena / prefijo mediante recorrido inorden."""
        subcadena = subcadena.lower()
        coincidencias = []
        def _inorden(nodo):
            if nodo:
                _inorden(nodo.izq)
                if subcadena in str(nodo.clave).lower():
                    coincidencias.extend(nodo.datos)
                _inorden(nodo.der)
        _inorden(self.raiz)
        return coincidencias

    def barrido_inorden(self):
        """Recorrido Inorden: devuelve elementos ordenados por clave de forma ascendente."""
        elementos = []
        def _inorden(nodo):
            if nodo:
                _inorden(nodo.izq)
                elementos.extend(nodo.datos)
                _inorden(nodo.der)
        _inorden(self.raiz)
        return elementos

    def barrido_por_nivel(self):
        """Recorrido en Amplitud (por niveles) utilizando una Cola (FIFO)."""
        if not self.raiz:
            return []
        resultado = []
        cola = [self.raiz]
        while cola:
            nodo = cola.pop(0)
            resultado.append((nodo.clave, nodo.datos))
            if nodo.izq:
                cola.append(nodo.izq)
            if nodo.der:
                cola.append(nodo.der)
        return resultado

    def obtener_conteo_tipos(self):
        """Recorre el árbol de tipos e informa el total de Pokémons por cada tipo."""
        res = []
        def _inorden(nodo):
            if nodo:
                _inorden(nodo.izq)
                res.append((nodo.clave, len(nodo.datos)))
                _inorden(nodo.der)
        _inorden(self.raiz)
        return res

# ==========================================
# CÁLCULOS Y RESOLUCIÓN DE CONSIGNAS
# ==========================================

def procesar_pokemons(path_json="lista.json"):
    # 1. Cargar archivo y construir los 3 árboles
    arbol_nombre = ArbolBinarioBusqueda()
    arbol_numero = ArbolBinarioBusqueda()
    arbol_tipo = ArbolBinarioBusqueda()
    
    with open(path_json, "r", encoding="utf-8") as f:
        pokemons = json.load(f)

    for p in pokemons:
        # Árbol 1: Índice por Nombre
        arbol_nombre.insertar(p["nombre"].lower(), p)
        
        # Árbol 2: Índice por Número
        arbol_numero.insertar(p["numero"], p)
        
        # Árbol 3: Índice por Tipo
        tipos = p.get("tipos", [])
        if isinstance(tipos, str):
            tipos = [tipos]
        for t in tipos:
            arbol_tipo.insertar(t.lower(), p)

    print("=== RESULTADOS Y OPERACIONES ===\n")

    # a) Mostrar Pokémons por número y por nombre (proximidad)
    print("--- 1. Búsqueda por número (ej. N° 6) ---")
    print(arbol_numero.buscar_exacto(6))
    
    print("\n--- 1. Búsqueda por proximidad de nombre ('bul' o 'gar') ---")
    resultados_proximidad = arbol_nombre.buscar_proximidad("gar") # Cambiado a 'gar' para que coincida con Gengar/Garchomp
    for p in resultados_proximidad:
        print(f"Nombre: {p['nombre']}, N°: {p['numero']}, Tipos: {p.get('tipos')}")

    # b) Mostrar Pokémons de tipos: Fantasma, Fuego, Acero y Eléctrico
    print("\n--- 2. Pokémons por Tipo (Fantasma, Fuego, Acero, Eléctrico) ---")
    for t in ["fantasma", "fuego", "acero", "eléctrico"]:
        poks = arbol_tipo.buscar_exacto(t)
        nombres = [p["nombre"] for p in poks]
        print(f"Tipo {t.capitalize()} ({len(nombres)}): {nombres}")

    # c) Listados
    print("\n--- 3. Listado Ascendente por Número ---")
    poks_orden_num = arbol_numero.barrido_inorden()
    for p in poks_orden_num[:10]:
        print(f"N° {p['numero']} - {p['nombre']}")

    print("\n--- 3. Listado Ascendente por Nombre ---")
    poks_orden_nom = arbol_nombre.barrido_inorden()
    for p in poks_orden_nom[:10]:
        print(f"- {p['nombre']} (N° {p['numero']})")

    print("\n--- 3. Listado por Nivel (Árbol de Nombres) ---")
    niveles = arbol_nombre.barrido_por_nivel()
    for clave, datos in niveles[:10]:
        print(f"Nodo '{clave}': {len(datos)} Pokémon(s)")

    # d) Pokémons débiles frente a Jolteon, Lycanroc y Tyrantrum
    print("\n--- 4. Débiles frente a Jolteon, Lycanroc y Tyrantrum ---")
    buscados = ["jolteon", "lycanroc", "tyrantrum"]
    tipos_atacantes = set()
    
    for b in buscados:
        for p in arbol_nombre.buscar_exacto(b):
            ts = p.get("tipos", [])
            for t in ts:
                tipos_atacantes.add(t.capitalize())
                
    debiles = set()
    for p in pokemons:
        debilidades = p.get("debilidades", [])
        if any(t in debilidades or t.lower() in [d.lower() for d in debilidades] for t in tipos_atacantes):
            debiles.add(p["nombre"])
            
    print(f"Tipos de ataque considerados: {tipos_atacantes}")
    lista_ordenada = sorted(debiles)
    print(f"Lista de Pokémons: {lista_ordenada}")

    # e) Conteo total de Pokémons por cada Tipo
    print("\n--- 5. Conteo de Pokémons por Tipo ---")
    for tipo, cantidad in arbol_tipo.obtener_conteo_tipos():
        print(f"- Tipo {tipo.capitalize()}: {cantidad} Pokémons")

    # f) Conteo Megaevolución y Gigamax
    megas = sum(1 for p in pokemons if p.get("tieneMegaEvolucion", False))
    gigamax = sum(1 for p in pokemons if p.get("tieneGigamax", False))
    
    print(f"\n--- 6. Pokémons con Megaevolución: {megas} ---")
    print(f"--- 7. Pokémons con forma Gigamax: {gigamax} ---")

if __name__ == "__main__":
    procesar_pokemons()