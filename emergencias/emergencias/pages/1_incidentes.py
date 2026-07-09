import streamlit as st
import csv
import time
from models.incident import Incident
from data_structures.hash_table import HashTable
from data_structures.priority_queue import PriorityQueue

st.set_page_config(page_title="Incidentes", page_icon="📋", layout="wide")
st.title("📋 Gestión de Incidentes")
st.markdown("---")

# ─── Inicializar estructuras en session_state ─────────────────────
if "hash_table" not in st.session_state:
    st.session_state.hash_table = HashTable()

if "priority_queue" not in st.session_state:
    st.session_state.priority_queue = PriorityQueue()

if "loaded" not in st.session_state:
    st.session_state.loaded = False

ht = st.session_state.hash_table
pq = st.session_state.priority_queue

# ─── Cargar CSV ───────────────────────────────────────────────────
st.subheader("📂 Cargar incidentes desde CSV")

if st.button("Cargar incidentes.csv"):
    ht2 = HashTable()
    pq2 = PriorityQueue()
    with open("data/incidentes.csv", newline="") as f:
        for row in csv.DictReader(f):
            inc = Incident(
                id        = row["ID"],
                ubicacion = row["Zona"],
                tipo      = row["Tipo"],
                severidad = int(row["Prioridad"]),
                timestamp = float(row["Timestamp"])
            )
            ht2.insert(inc)
            pq2.enqueue(inc)
    st.session_state.hash_table     = ht2
    st.session_state.priority_queue = pq2
    st.session_state.loaded         = True
    st.success(f"✅ {ht2.size} incidentes cargados correctamente")

# ─── Registrar nuevo incidente ────────────────────────────────────
st.markdown("---")
st.subheader("➕ Registrar nuevo incidente")

col1, col2 = st.columns(2)

with col1:
    nuevo_id   = st.text_input("ID", placeholder="I-0501")
    nueva_zona = st.selectbox("Zona", [f"Zona_{i}" for i in range(1, 51)])
    nuevo_tipo = st.selectbox("Tipo", ["incendio", "derrumbe", "herido", "inundacion", "rescate"])

with col2:
    nueva_severidad = st.slider("Severidad", 1, 10, 5)
    st.markdown("<br>", unsafe_allow_html=True)
    registrar = st.button("Registrar incidente")

if registrar:
    if not nuevo_id:
        st.error("El ID es obligatorio")
    elif st.session_state.hash_table.search(nuevo_id):
        st.error(f"Ya existe un incidente con ID {nuevo_id}")
    else:
        inc = Incident(
            id        = nuevo_id,
            ubicacion = nueva_zona,
            tipo      = nuevo_tipo,
            severidad = nueva_severidad,
            timestamp = time.time()
        )
        st.session_state.hash_table.insert(inc)
        st.session_state.priority_queue.enqueue(inc)
        st.success(f"✅ Incidente {nuevo_id} registrado con prioridad {inc.prioridad}")

# ─── Buscar incidente ─────────────────────────────────────────────
st.markdown("---")
st.subheader("🔍 Buscar incidente por ID")

col1, col2 = st.columns([3, 1])
with col1:
    buscar_id = st.text_input("ID a buscar", placeholder="I-0001")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    buscar = st.button("Buscar")

if buscar:
    resultado = st.session_state.hash_table.search(buscar_id)
    if resultado:
        st.success(f"Incidente encontrado")
        col1, col2, col3 = st.columns(3)
        col1.metric("ID",        resultado.id)
        col2.metric("Zona",      resultado.ubicacion)
        col3.metric("Tipo",      resultado.tipo)
        col1.metric("Prioridad", resultado.prioridad)
        col2.metric("Severidad", resultado.severidad)
        col3.metric("Estado",    resultado.estado)
    else:
        st.error(f"No se encontró el incidente {buscar_id}")

# ─── Estadísticas Hash Table ──────────────────────────────────────
st.markdown("---")
st.subheader("📊 Estadísticas Hash Table")

stats = st.session_state.hash_table.get_stats()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total incidentes", stats["size"])
col2.metric("Factor de carga",  stats["factor_carga"])
col3.metric("Colisiones",       stats["colisiones"])
col4.metric("Buckets usados",   stats["buckets_utilizados"])

# ─── Tabla de incidentes ──────────────────────────────────────────
st.markdown("---")
st.subheader("📋 Incidentes registrados")

if st.session_state.hash_table.size > 0:
    todos = st.session_state.hash_table.get_all()
    data  = [{
        "ID"       : inc.id,
        "Zona"     : inc.ubicacion,
        "Tipo"     : inc.tipo,
        "Severidad": inc.severidad,
        "Prioridad": inc.prioridad,
        "Estado"   : inc.estado
    } for inc in todos]
    st.dataframe(data, use_container_width=True)
else:
    st.info("No hay incidentes cargados. Carga el CSV o registra uno nuevo.")