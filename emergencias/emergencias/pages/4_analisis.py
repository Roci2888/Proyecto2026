import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import time
import copy
from data_structures.hash_table import HashTable
from data_structures.heap import MaxHeap
from models.road_network import RoadNetwork
from models.emergency_center import EmergencyCenter

st.set_page_config(page_title="Análisis", page_icon="📊", layout="wide")
st.title("📊 Análisis Experimental")
st.markdown("---")

CENTERS = [
    EmergencyCenter("C1", "Centro Norte", "Centro_Norte"),
    EmergencyCenter("C2", "Centro Sur",   "Centro_Sur"),
    EmergencyCenter("C3", "Centro Este",  "Centro_Este"),
    EmergencyCenter("C4", "Centro Oeste", "Centro_Oeste"),
]

# ─── Verificar incidentes cargados ────────────────────────────────
if "hash_table" not in st.session_state or st.session_state.hash_table.size == 0:
    st.warning("⚠️ Primero carga los incidentes en la página de Incidentes")
    st.stop()

todos = st.session_state.hash_table.get_all()

# ─── Sección 1: Hashing ───────────────────────────────────────────
st.subheader("1️⃣ Análisis Hash Table")

if st.button("Analizar Hashing"):
    sizes      = [100, 200, 300, 400, 500]
    colisiones = []
    factores   = []
    tiempos    = []

    for n in sizes:
        ht = HashTable()
        t0 = time.perf_counter()
        for inc in todos[:n]:
            ht.insert(inc)
        t = time.perf_counter() - t0

        stats = ht.get_stats()
        colisiones.append(stats["colisiones"])
        factores.append(stats["factor_carga"])
        tiempos.append(round(t, 6))

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=sizes, y=colisiones,
            mode="lines+markers",
            name="Colisiones",
            line=dict(color="red")
        ))
        fig.update_layout(
            title="Colisiones vs cantidad de incidentes",
            xaxis_title="Incidentes insertados",
            yaxis_title="Colisiones"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=sizes, y=factores,
            mode="lines+markers",
            name="Factor de carga",
            line=dict(color="blue")
        ))
        fig2.add_hline(
            y=0.75,
            line_dash="dash",
            line_color="orange",
            annotation_text="Límite rehash (0.75)"
        )
        fig2.update_layout(
            title="Factor de carga vs cantidad de incidentes",
            xaxis_title="Incidentes insertados",
            yaxis_title="Factor de carga"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### Resumen")
    data = [{
        "n"            : n,
        "Colisiones"   : c,
        "Factor carga" : f,
        "Tiempo (s)"   : t
    } for n, c, f, t in zip(sizes, colisiones, factores, tiempos)]
    st.dataframe(data, use_container_width=True)

st.markdown("---")

# ─── Sección 2: Heap ──────────────────────────────────────────────
st.subheader("2️⃣ Análisis Heap")

if st.button("Analizar Heap"):
    sizes        = [100, 200, 300, 400, 500]
    t_insercion  = []
    t_extraccion = []

    for n in sizes:
        heap = MaxHeap()

        # Tiempo inserción
        t0 = time.perf_counter()
        for inc in todos[:n]:
            heap.insert(inc)
        t_insercion.append(round(time.perf_counter() - t0, 6))

        # Tiempo extracción
        heap2 = MaxHeap()
        heap2._data = copy.deepcopy(heap._data)
        t0 = time.perf_counter()
        for _ in range(n):
            heap2.extract_max()
        t_extraccion.append(round(time.perf_counter() - t0, 6))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sizes, y=t_insercion,
        mode="lines+markers",
        name="Inserción",
        line=dict(color="green")
    ))
    fig.add_trace(go.Scatter(
        x=sizes, y=t_extraccion,
        mode="lines+markers",
        name="Extracción",
        line=dict(color="purple")
    ))
    fig.update_layout(
        title="Heap: tiempo de inserción vs extracción",
        xaxis_title="Cantidad de incidentes",
        yaxis_title="Tiempo (segundos)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Resumen")
    data = [{
        "n"              : n,
        "Inserción (s)"  : ti,
        "Extracción (s)" : te
    } for n, ti, te in zip(sizes, t_insercion, t_extraccion)]
    st.dataframe(data, use_container_width=True)

st.markdown("---")

# ─── Sección 3: Grafos ────────────────────────────────────────────
st.subheader("3️⃣ Análisis Grafos — BFS vs Dijkstra vs A*")

if not st.session_state.get("graph_loaded"):
    st.warning("⚠️ Primero carga la red vial en la página de Rutas")
else:
    if st.button("Analizar Grafos"):
        rn    = st.session_state.road_network
        zonas = sorted(list(rn.get_nodes()))

        resultados = []
        def heuristica(a, b):
            num_a = int(a.replace("Zona_", "")) if "Zona_" in a else 0
            num_b = int(b.replace("Zona_", "")) if "Zona_" in b else 0
            return abs(num_a - num_b)
       

        for center in CENTERS:
            for destino in zonas[:10]:
                if center.ubicacion == destino:
                    continue

                # BFS
                t0 = time.perf_counter()
                ruta_bfs, vis_bfs = rn.bfs(center.ubicacion, destino)
                t_bfs = round(time.perf_counter() - t0, 6)

                # Dijkstra
                t0 = time.perf_counter()
                ruta_dij, costo, vis_dij = rn.dijkstra(center.ubicacion, destino)
                t_dij = round(time.perf_counter() - t0, 6)

                # A*
                t0 = time.perf_counter()
                ruta_astar, costo_astar, vis_astar = rn.a_star(center.ubicacion, destino, heuristica)
                t_astar = round(time.perf_counter() - t0, 6)

                resultados.append({
                    "Centro"           : center.nombre,
                    "Destino"          : destino,
                    "BFS nodos"        : len(vis_bfs),
                    "Dijkstra nodos"   : len(vis_dij),
                    "A* nodos"         : len(vis_astar),
                    "BFS tiempo (s)"   : t_bfs,
                    "Dijkstra tiempo"  : t_dij,
                    "A* tiempo"        : t_astar,
                    "Costo Dijkstra"   : costo,
                    "Costo A*"         : costo_astar
                })

        st.dataframe(resultados, use_container_width=True)

        # Gráfico comparativo
        fig = go.Figure()
        destinos = [r["Destino"] for r in resultados[:10]]
        fig.add_trace(go.Bar(
            name="BFS nodos visitados",
            x=destinos,
            y=[r["BFS nodos"] for r in resultados[:10]],
            marker_color="blue"
        ))
        fig.add_trace(go.Bar(
            name="Dijkstra nodos visitados",
            x=destinos,
            y=[r["Dijkstra nodos"] for r in resultados[:10]],
            marker_color="red"
        ))
        fig.add_trace(go.Bar(
            name="A* nodos visitados",
            x=destinos,
            y=[r["A* nodos"] for r in resultados[:10]],
            marker_color="green"
        ))
        fig.update_layout(
            title="BFS vs Dijkstra vs A*: nodos visitados",
            xaxis_title="Destino",
            yaxis_title="Nodos visitados",
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True)