import streamlit as st
import plotly.graph_objects as go
from algorithms.sorting import (
    sort_by_timestamp,
    sort_by_priority,
    sort_by_zone,
    benchmark
)

st.set_page_config(page_title="Sorting", page_icon="🔃", layout="wide")
st.title("🔃 Ordenamiento de Incidentes")
st.markdown("---")

# ─── Verificar incidentes cargados ───────────────────────────────
if "hash_table" not in st.session_state or st.session_state.hash_table.size == 0:
    st.warning("⚠️ Primero carga los incidentes en la página de Incidentes")
    st.stop()

todos = st.session_state.hash_table.get_all()

# ─── Reportes ordenados ───────────────────────────────────────────
st.subheader("📋 Reportes ordenados")

col1, col2 = st.columns(2)

with col1:
    reporte = st.selectbox("Tipo de reporte", [
        "Incidentes más antiguos",
        "Incidentes más críticos",
        "Zonas con más incidentes"
    ])

with col2:
    algoritmo = st.selectbox("Algoritmo", ["MergeSort", "QuickSort"])

algo = "merge" if algoritmo == "MergeSort" else "quick"

if st.button("Generar reporte"):
    if reporte == "Incidentes más antiguos":
        resultado = sort_by_timestamp(todos, algorithm=algo)
        data = [{
            "ID"       : inc.id,
            "Zona"     : inc.ubicacion,
            "Tipo"     : inc.tipo,
            "Timestamp": inc.timestamp,
            "Estado"   : inc.estado
        } for inc in resultado[:50]]
        st.dataframe(data, use_container_width=True)

    elif reporte == "Incidentes más críticos":
        resultado = sort_by_priority(todos, algorithm=algo)
        data = [{
            "ID"       : inc.id,
            "Zona"     : inc.ubicacion,
            "Tipo"     : inc.tipo,
            "Prioridad": inc.prioridad,
            "Estado"   : inc.estado
        } for inc in resultado[:50]]
        st.dataframe(data, use_container_width=True)

    else:
        resultado = sort_by_zone(todos, algorithm=algo)
        st.dataframe(resultado, use_container_width=True)

# ─── Benchmark ────────────────────────────────────────────────────
st.markdown("---")
st.subheader("⚡ Comparación MergeSort vs QuickSort")

if st.button("Ejecutar benchmark"):
    sizes   = [100, 200, 300, 400, 500]
    t_merge = []
    t_quick = []

    for n in sizes:
        subset  = todos[:n]
        result  = benchmark(subset)
        t_merge.append(result["merge_sort_s"])
        t_quick.append(result["quick_sort_s"])

    # Gráfico
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sizes, y=t_merge,
        mode="lines+markers",
        name="MergeSort",
        line=dict(color="blue")
    ))
    fig.add_trace(go.Scatter(
        x=sizes, y=t_quick,
        mode="lines+markers",
        name="QuickSort",
        line=dict(color="red")
    ))
    fig.update_layout(
        title     = "MergeSort vs QuickSort",
        xaxis_title = "Cantidad de incidentes",
        yaxis_title = "Tiempo (segundos)",
        legend_title = "Algoritmo"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Tabla resumen
    st.markdown("#### Resumen")
    data = [{
        "n"           : n,
        "MergeSort(s)": tm,
        "QuickSort(s)": tq,
        "Ganador"     : "MergeSort" if tm < tq else "QuickSort"
    } for n, tm, tq in zip(sizes, t_merge, t_quick)]
    st.dataframe(data, use_container_width=True)