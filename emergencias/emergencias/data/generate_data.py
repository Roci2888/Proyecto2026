import csv
import random
import time
import json

TIPOS   = ["incendio", "derrumbe", "herido", "inundacion", "rescate"]
ZONAS   = [f"Zona_{i}" for i in range(1, 51)]
CENTROS = ["Centro_Norte", "Centro_Sur", "Centro_Este", "Centro_Oeste"]

def generate_incidents(n=500, filename="data/incidentes.csv"):
    now = time.time()
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["ID", "Zona", "Prioridad", "Tipo", "Timestamp"])
        writer.writeheader()
        for i in range(n):
            writer.writerow({
                "ID"       : f"I-{i+1:04d}",
                "Zona"     : random.choice(ZONAS),
                "Prioridad": random.randint(1, 10),
                "Tipo"     : random.choice(TIPOS),
                "Timestamp": round(now - random.uniform(0, 86400), 2)
            })
    print(f"{n} incidentes generados en {filename}")

def generate_graph(nodes=50, edges=100, filename="data/red_vial.json"):
    node_list = ZONAS.copy()
    edge_list = []
    edge_set  = set()

    def add_edge(a, b, weight):
        if (a, b) not in edge_set:
            edge_list.append({"from": a, "to": b, "weight": weight})
            edge_set.add((a, b))
        if (b, a) not in edge_set:
            edge_list.append({"from": b, "to": a, "weight": weight})
            edge_set.add((b, a))

    # Árbol spanning para garantizar conectividad
    for i in range(1, nodes):
        origen  = node_list[random.randint(0, i - 1)]
        destino = node_list[i]
        peso    = random.randint(5, 60)
        add_edge(origen, destino, peso)

    # Aristas adicionales
    intentos = 0
    while len(edge_list) < edges * 2 and intentos < 1000:
        a, b = random.sample(node_list, 2)
        add_edge(a, b, random.randint(5, 60))
        intentos += 1

    # Centros como nodos reales conectados a zonas cercanas
    for zona in ["Zona_1", "Zona_2", "Zona_3"]:
        add_edge("Centro_Norte", zona, random.randint(5, 15))

    for zona in ["Zona_13", "Zona_14", "Zona_15"]:
        add_edge("Centro_Sur", zona, random.randint(5, 15))

    for zona in ["Zona_26", "Zona_27", "Zona_28"]:
        add_edge("Centro_Este", zona, random.randint(5, 15))

    for zona in ["Zona_39", "Zona_40", "Zona_41"]:
        add_edge("Centro_Oeste", zona, random.randint(5, 15))

    all_nodes = node_list + CENTROS

    with open(filename, "w") as f:
        json.dump({"nodes": all_nodes, "edges": edge_list}, f, indent=2)

    print(f"Grafo generado en {filename}")
    print(f"   Nodos : {len(all_nodes)} (50 zonas + 4 centros)")
    print(f"   Aristas: {len(edge_list)}")

if __name__ == "__main__":
    # generate_incidents()  ← comentado, incidentes ya están generados
    generate_graph()

