import streamlit as st

st.set_page_config(
    page_title="Sistema de Emergencias",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Sistema Inteligente de Gestión de Emergencias")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 📋 Incidentes\nRegistrar y gestionar incidentes de emergencia")

with col2:
    st.warning("### 🗺️ Rutas\nCalcular rutas óptimas hacia los incidentes")

with col3:
    st.success("### 📊 Análisis\nEstadísticas y rendimiento del sistema")

st.markdown("---")
st.markdown("Usa el **menú lateral** para navegar entre las secciones.")