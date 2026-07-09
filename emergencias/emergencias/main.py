import csv
import time
from models.incident          import Incident
from models.emergency_center  import EmergencyCenter
from models.road_network      import RoadNetwork
from data_structures.hash_table   import HashTable
from data_structures.priority_queue import PriorityQueue

# ─── Centros de emergencia definidos en código ────────────────────

CENTERS = [
    EmergencyCenter("C1", "Centro Norte", "Centro_Norte"),
    EmergencyCenter("C2", "Centro Sur",   "Centro_Sur"),
    EmergencyCenter("C3", "Centro Este",  "Centro_Este"),
    EmergencyCenter("C4", "Centro Oeste", "Centro_Oeste"),
]

# ─── Paso 1: Cargar incidentes desde CSV ─────────────────────────

def load_incidents(path: str, hash_table: HashTable, priority_queue: PriorityQueue) -> None:
    """
    Lee incidentes.csv e inserta cada uno en la
    Hash Table y la Priority Queue.
    Complejidad: O(n)
    """
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            incident = Incident(
                id        = row["ID"],
                ubicacion = row["Zona"],
                tipo      = row["Tipo"],
                severidad = int(row["Prioridad"]),
                timestamp = float(row["Timestamp"])
            )
            hash_table.insert(incident)      # Paso 2a
            priority_queue.enqueue(incident) # Paso 2b

# ─── Paso 4: Buscar ruta óptima ──────────────────────────────────

def find_best_route(incident: Incident, road_network: RoadNetwork) -> tuple:
    """
    Busca la ruta óptima desde el centro más cercano
    hasta el incidente usando Dijkstra.
    Complejidad: O(C × (V + E) log V) donde C = cantidad de centros
    """
    best_route  = None
    best_cost   = float('inf')
    best_center = None
    best_visited = []

    for center in CENTERS:
        route, cost, visited = road_network.dijkstra(
            center.ubicacion,
            incident.ubicacion
        )
        if route and cost < best_cost:
            best_route   = route
            best_cost    = cost
            best_center  = center
            best_visited = visited

    return best_route, best_cost, best_center, best_visited

# ─── Escenario integrado ──────────────────────────────────────────

def run():
    print("=" * 55)
    print("   SISTEMA DE GESTIÓN DE EMERGENCIAS")
    print("=" * 55)

    # Inicializar estructuras
    hash_table     = HashTable()
    priority_queue = PriorityQueue()
    road_network   = RoadNetwork()

    # ── Paso 1: Leer incidentes.csv ──
    print("\n[Paso 1] Cargando incidentes...")
    load_incidents("data/incidentes.csv", hash_table, priority_queue)
    print(f"         {hash_table.size} incidentes cargados")

    # ── Paso 2: Mostrar stats Hash Table ──
    print("\n[Paso 2] Estadísticas Hash Table:")
    stats = hash_table.get_stats()
    for k, v in stats.items():
        print(f"         {k:<22}: {v}")

    # ── Paso 3: Extraer incidente más urgente ──
    print("\n[Paso 3] Extrayendo incidente más urgente...")
    urgent = priority_queue.dequeue()
    print(f"         ID       : {urgent.id}")
    print(f"         Zona     : {urgent.ubicacion}")
    print(f"         Tipo     : {urgent.tipo}")
    print(f"         Prioridad: {urgent.prioridad}")
    print(f"         Estado   : {urgent.estado}")

    # ── Paso 4: Cargar red vial y buscar ruta ──
    print("\n[Paso 4] Cargando red vial...")
    road_network.load_from_json("data/red_vial.json")
    print(f"         {road_network}")

    print("\n[Paso 4] Buscando ruta óptima...")
    route, best_cost, best_center, visited = find_best_route(urgent, road_network)

    # ── Paso 5: Mostrar resultado ──
    print("\n[Paso 5] Resultado:")
    print("-" * 55)
    if route:
        print(f"  Centro asignado : {best_center.nombre}")
        print(f"  Incidente       : {urgent.id} ({urgent.tipo})")
        print(f"  Prioridad       : {urgent.prioridad}")
        print(f"  Nodos visitados : {len(visited)}")
        print(f"  Ruta sugerida   : {' → '.join(route)}")
        print(f"  Costo total     : {best_cost} min")
        print(f"  Tiempo estimado : {best_cost} minutos")

        # ── Vuelta: buscar centro más cercano desde el incidente ──
        print("\n[Vuelta] Buscando centro más cercano para regresar...")
        best_return_route  = None
        best_return_cost   = float('inf')
        best_return_center = None

        for center in CENTERS:
            return_route, return_cost, _ = road_network.dijkstra(
                urgent.ubicacion,    # parte desde la zona del incidente
                center.ubicacion     # hacia cada centro
            )
            if return_route and return_cost < best_return_cost:
                best_return_route  = return_route
                best_return_cost   = return_cost
                best_return_center = center

        if best_return_route:
            print(f"  Centro más cercano: {best_return_center.nombre}")
            print(f"  Ruta de vuelta    : {' → '.join(best_return_route)}")
            print(f"  Costo de vuelta   : {best_return_cost} min")
        else:
            print("No se encontró ruta de vuelta")
    else:
        print("No se encontró ruta disponible")

    print("-" * 55)
    print("\n Escenario integrado completado")
