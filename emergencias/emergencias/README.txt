=======================================================
   SISTEMA DE GESTIÓN DE EMERGENCIAS
   Proyecto Integrador Final
=======================================================

REQUISITOS
----------
- Python 3.10 o superior
- pip

INSTALACIÓN
-----------
1. Descomprime el archivo RAR
2. Abre el cmd y navega a la carpeta emergencias:

   cd C:\ruta\donde\descomprimiste\emergencias

3. Instala las dependencias:

   pip install -r requirements.txt

4. Genera los datos iniciales:

   python data/generate_data.py

EJECUCIÓN
---------
Interfaz visual (Streamlit):

   streamlit run app.py

Escenario integrado (consola):

   python main.py

ORDEN DE USO EN LA INTERFAZ
----------------------------
1. Página "Incidentes"  → cargar incidentes.csv
2. Página "Rutas"       → cargar red_vial.json
3. Página "Sorting"     → generar reportes
4. Página "Análisis"    → ver benchmarks y gráficos

ESTRUCTURA DEL PROYECTO
------------------------
models/           → ADTs (Incident, EmergencyCenter, RoadNetwork)
data_structures/  → Hash Table, Heap, Priority Queue
algorithms/       → MergeSort, QuickSort
data/             → incidentes.csv, red_vial.json
pages/            → páginas Streamlit
app.py            → punto de entrada Streamlit
main.py           → escenario integrado