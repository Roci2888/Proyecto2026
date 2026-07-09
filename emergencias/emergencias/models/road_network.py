from collections import defaultdict, deque
import heapq
import csv
import json
from os import path

class RoadNetwork:
    """
    ADT RoadNetwork: representa la red vial como un grafo dirigido ponderado.

    Atributos:
        _adj  (dict): lista de adyacencia {nodo: [(vecino, peso)]}
        _nodes(set) : conjunto de nodos del grafo

    Precondiciones:
        - Los nodos deben ser strings no vacíos
        - El peso de las aristas debe ser mayor a 0

    Postcondiciones:
        - El grafo queda construido y listo para búsqueda de rutas
    
    Complejidades:
        - add_node  : O(1)
        - add_edge  : O(1)
        - bfs       : O(V + E)
        - dijkstra  : O((V + E) log V)
        - a_star    : O((V + E) log V)
    """

    def __init__(self):
        self._adj   = defaultdict(list)
        self._nodes = set()

    # ─── Construcción del grafo ───────────────────────────────────

    def add_node(self, node: str) -> None:
        """
        Agrega un nodo al grafo.
        Precondición : node no debe estar vacío
        Postcondición: node queda en el conjunto de nodos
        Complejidad  : O(1)
        """
        if not node:
            raise ValueError("El nodo no puede estar vacío")
        self._nodes.add(node)

    def add_edge(self, origin: str, dest: str, weight: float) -> None:
        """
        Agrega una arista dirigida ponderada.
        Precondición : weight debe ser mayor a 0
        Postcondición: arista queda en la lista de adyacencia
        Complejidad  : O(1)
        """
        if weight <= 0:
            raise ValueError("El peso debe ser mayor a 0")
        self._nodes.update([origin, dest])
        self._adj[origin].append((dest, weight))

    def load_from_csv(self, path: str) -> None:
        """
        Carga el grafo desde un archivo CSV.
        Formato esperado: origen,destino,peso
        Complejidad: O(E)
        """
        with open(path) as f:
            for row in csv.DictReader(f):
                self.add_edge(row["origen"], row["destino"], float(row["peso"]))
        print(f"Grafo cargado desde {path}")

    def load_from_json(self, path: str) -> None:
        """
        Carga el grafo desde un archivo JSON.
        Formato esperado: {"nodes": [...], "edges": [{"from","to","weight"}]}
        Complejidad: O(V + E)
        """
        with open(path) as f:
         data = json.load(f)
        for node in data.get("nodes", []):
         self.add_node(node)
        for edge in data.get("edges", []):
         self.add_edge(edge["from"], edge["to"], edge["weight"])




    # ─── Algoritmos de búsqueda ───────────────────────────────────

    def bfs(self, start: str, goal: str) -> tuple:
        """
        Búsqueda en anchura — encuentra ruta con menos saltos.
        Precondición : start y goal deben existir en el grafo
        Postcondición: retorna (ruta, nodos_visitados)
        Complejidad  : O(V + E)
        """
        if start not in self._nodes or goal not in self._nodes:
            return None, []

        visited       = {start: None}
        queue         = deque([start])
        nodes_visited = []

        while queue:
            node = queue.popleft()
            nodes_visited.append(node)

            if node == goal:
                return self._reconstruct(visited, start, goal), nodes_visited

            for neighbor, _ in self._adj[node]:
                if neighbor not in visited:
                    visited[neighbor] = node
                    queue.append(neighbor)

        return None, nodes_visited

    def dijkstra(self, start: str, goal: str) -> tuple:
        """
        Algoritmo de Dijkstra — encuentra ruta de menor costo.
        Precondición : start y goal deben existir en el grafo
        Postcondición: retorna (ruta, costo_total, nodos_visitados)
        Complejidad  : O((V + E) log V)
        """
        if start not in self._nodes or goal not in self._nodes:
            return None, float('inf'), []

        dist          = {start: 0}
        prev          = {start: None}
        pq            = [(0, start)]
        nodes_visited = []

        while pq:
            cost, node = heapq.heappop(pq)

            if node in nodes_visited:
                continue
            nodes_visited.append(node)

            if node == goal:
                return self._reconstruct(prev, start, goal), cost, nodes_visited

            for neighbor, weight in self._adj[node]:
                new_cost = cost + weight
                if neighbor not in dist or new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    prev[neighbor] = node
                    heapq.heappush(pq, (new_cost, neighbor))

        return None, float('inf'), nodes_visited

    def a_star(self, start: str, goal: str, heuristic) -> tuple:
        """
        Algoritmo A* — encuentra ruta óptima con heurística.
        Precondición : start y goal deben existir, heuristic debe ser admisible
        Postcondición: retorna (ruta, costo_total, nodos_visitados)
        Complejidad  : O((V + E) log V)
        """
        if start not in self._nodes or goal not in self._nodes:
            return None, float('inf'), []

        open_set      = [(heuristic(start, goal), 0, start)]
        prev          = {start: None}
        g_cost        = {start: 0}
        nodes_visited = []

        while open_set:
            _, cost, node = heapq.heappop(open_set)

            if node in nodes_visited:
                continue
            nodes_visited.append(node)

            if node == goal:
                return self._reconstruct(prev, start, goal), cost, nodes_visited

            for neighbor, weight in self._adj[node]:
                new_g = g_cost[node] + weight
                if neighbor not in g_cost or new_g < g_cost[neighbor]:
                    g_cost[neighbor] = new_g
                    prev[neighbor]   = node
                    f = new_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, new_g, neighbor))

        return None, float('inf'), nodes_visited

    # ─── Utilidades ───────────────────────────────────────────────

    def _reconstruct(self, prev: dict, start: str, goal: str):
        """Reconstruye la ruta desde el diccionario de predecesores."""
        path, node = [], goal
        while node is not None:
            path.append(node)
            node = prev.get(node)
        path.reverse()
        return path if path[0] == start else None

    def get_nodes(self) -> set:
        """Retorna el conjunto de nodos. Complejidad: O(1)"""
        return self._nodes

    def get_neighbors(self, node: str) -> list:
        """Retorna los vecinos de un nodo. Complejidad: O(1)"""
        return self._adj[node]

    def __repr__(self):
        return (f"RoadNetwork(nodos={len(self._nodes)}, "
                f"aristas={sum(len(v) for v in self._adj.values())})")