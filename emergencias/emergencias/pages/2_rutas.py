import streamlit as st
from models.road_network import RoadNetwork
from models.emergency_center import EmergencyCenter

st.set_page_config(page_title="Rutas", page_icon="🗺️", layout="wide")
st.title("🗺️ Cálculo de Rutas")
st.markdown("---")

# ─── Centros de emergencia ────────────────────────────────────────
CENTERS = [
    EmergencyCenter("C1", "Centro Norte", "Centro_Norte"),
    EmergencyCenter("C2", "Centro Sur",   "Centro_Sur"),
    EmergencyCenter("C3", "Centro Este",  "Centro_Este"),
    EmergencyCenter("C4", "Centro Oeste", "Centro_Oeste"),
]

# ─── Inicializar red vial ─────────────────────────────────────────
if "road_network" not in st.session_state:
    st.session_state.road_network  = None
if "graph_loaded" not in st.session_state:
    st.session_state.graph_loaded = False

# ─── Cargar grafo ─────────────────────────────────────────────────
st.subheader("📂 Cargar red vial")

if st.button("Cargar red_vial.json"):
    rn = RoadNetwork()
    rn.load_from_json("data/red_vial.json")
    st.session_state.road_network  = rn
    st.session_state.graph_loaded = True
    st.success(f"{rn}")

# ─── Calcular ruta ────────────────────────────────────────────────
st.markdown("---")
st.subheader("🔍 Calcular ruta óptima")

if not st.session_state.graph_loaded:
    st.warning("⚠️ Primero carga la red vial")
else:
    rn     = st.session_state.road_network
    zonas  = sorted(list(rn.get_nodes()))

    col1, col2, col3 = st.columns(3)

    with col1:
        centro_sel = st.selectbox(
            "Centro de emergencia",
            [c.nombre for c in CENTERS]
        )
    with col2:
        destino = st.selectbox("Zona destino", zonas)
    with col3:
        algoritmo = st.selectbox("Algoritmo", ["Dijkstra", "BFS", "A*"])

    buscar = st.button("Calcular ruta")

    if buscar:
        centro = next(c for c in CENTERS if c.nombre == centro_sel)

        def heuristica(a: str, b: str) -> float:
            # Heurística basada en diferencia de número de zona
            num_a = int(a.replace("Zona_", "")) if "Zona_" in a else 0
            num_b = int(b.replace("Zona_", "")) if "Zona_" in b else 0
            return abs(num_a - num_b)

        if algoritmo == "Dijkstra":
            ruta, costo, visitados = rn.dijkstra(centro.ubicacion, destino)
        elif algoritmo == "BFS":
            ruta, visitados = rn.bfs(centro.ubicacion, destino)
            costo = len(ruta) - 1 if ruta else 0
        else:  # A*
            ruta, costo, visitados = rn.a_star(centro.ubicacion, destino, heuristica)

        st.markdown("---")

        if ruta:
            col1, col2, col3 = st.columns(3)
            col1.metric("Nodos visitados", len(visitados))
            col2.metric("Paradas en ruta", len(ruta))
            col3.metric(
                "Costo total",
                f"{costo} min" if algoritmo == "Dijkstra" else f"{costo} saltos"
            )

            st.markdown("#### Ruta encontrada")
            st.success(" → ".join(ruta))

            st.markdown("#### Nodos visitados")
            st.info(" → ".join(visitados))
        else:
            st.error("No se encontró ruta entre los puntos seleccionados")

# ─── Incidente más urgente ────────────────────────────────────────
st.markdown("---")
st.subheader("🚨 Ruta al incidente más urgente")

if not st.session_state.graph_loaded:
    st.warning("⚠️ Primero carga la red vial en la página anterior")
elif "priority_queue" not in st.session_state or st.session_state.priority_queue.is_empty():
    st.warning("⚠️ Primero carga los incidentes en la página de Incidentes")
else:
    if st.button("Calcular ruta al incidente más urgente"):
        pq      = st.session_state.priority_queue
        rn      = st.session_state.road_network
        urgente = pq.peek()

        # ── Ida: buscar centro más cercano al incidente ──
        best_route   = None
        best_cost    = float('inf')
        best_center  = None
        best_visited = []

        for center in CENTERS:
            ruta, costo, visitados = rn.dijkstra(
                center.ubicacion,
                urgente.ubicacion
            )
            if ruta and costo < best_cost:
                best_route   = ruta
                best_cost    = costo
                best_center  = center
                best_visited = visitados

        if best_route:
            st.markdown("#### 🚑 Incidente más urgente")
            col1, col2, col3 = st.columns(3)
            col1.metric("ID",        urgente.id)
            col2.metric("Zona",      urgente.ubicacion)
            col3.metric("Prioridad", urgente.prioridad)

            st.markdown("#### ➡️ Ruta de ida")
            col1, col2, col3 = st.columns(3)
            col1.metric("Centro asignado",  best_center.nombre)
            col2.metric("Costo total",      f"{best_cost} min")
            col3.metric("Nodos visitados",  len(best_visited))
            st.success(" → ".join(best_route))

            # ── Vuelta: buscar centro más cercano desde el incidente ──
            best_return_route  = None
            best_return_cost   = float('inf')
            best_return_center = None

            for center in CENTERS:
                return_route, return_cost, _ = rn.dijkstra(
                    urgente.ubicacion,
                    center.ubicacion
                )
                if return_route and return_cost < best_return_cost:
                    best_return_route  = return_route
                    best_return_cost   = return_cost
                    best_return_center = center

            if best_return_route:
                st.markdown("#### ⬅️ Ruta de vuelta")
                col1, col2, col3 = st.columns(3)
                col1.metric("Centro más cercano", best_return_center.nombre)
                col2.metric("Costo de vuelta",    f"{best_return_cost} min")
                col3.metric("Total ida + vuelta",  f"{best_cost + best_return_cost} min")
                st.info(" → ".join(best_return_route))
        else:
            st.error("No se encontró ruta disponible")

