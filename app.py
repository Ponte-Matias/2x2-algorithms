import streamlit as st
from openpyxl import load_workbook
import random
from algoritmo_inversor import invertir_alg

# Función que obtiene todas las celdas que ocupa verticalmente una combinación de celdas
# (las que están en la primer fila e indican el subset)
def obtener_rango_combinado_y_valores(hoja, valor_buscado):

    rango_vertical = None

    # Paso 1: Buscar la celda combinada que contiene el valor buscado
    for rango in hoja.merged_cells.ranges:
        celda_inicial = hoja[rango.coord.split(":")[0]]
        if celda_inicial.value == valor_buscado:
            rango_vertical = rango
            break

    if rango_vertical is None:
        raise ValueError(f"No se encontró una celda combinada con el valor '{valor_buscado}'")

    # Paso 2: Extraer coordenadas del rango (ej: A3:A8)
    start_cell, end_cell = str(rango_vertical).split(":")
    start_col = hoja[start_cell].column_letter
    start_row = hoja[start_cell].row
    end_row = hoja[end_cell].row

    # Paso 3: Recorrer columnas B en adelante, en esas filas
    datos = []

    for fila in range(start_row, end_row + 1):
        for columna in range(2, hoja.max_column + 1):  # columna 2 = B
            celda = hoja.cell(row=fila, column=columna)
            if celda.value is not None:
                datos.append({
                    "fila": fila,
                    "columna": celda.column_letter,
                    "algoritmo": celda.value
                })

    return datos

# Cargar wb de forma estática ya que nunca cambia
@st.cache_resource
def cargar_workbook(nombre_archivo):
    wb = load_workbook(nombre_archivo, data_only=True)
    return wb

# Ruta al archivo Excel
archivo = "algs.xlsx"
# Usar el workbook cargado
wb = cargar_workbook(archivo)

st.title("2x2 Set-Up Algorithms")

metodo = st.sidebar.selectbox("Method: ", wb.sheetnames)
# Escoger el método, acceder a la hoja correspondiente
# Guardar la hoja si cambió el método
if "metodo_actual" not in st.session_state or st.session_state.metodo_actual != metodo:
    st.session_state.metodo_actual = metodo
    st.session_state.hoja_actual = wb[metodo]

# Usar la hoja desde session_state
hoja = st.session_state.hoja_actual

# Recorrer la columna A (columna 1), ignorando celdas vacías
subsets = []    # Lista con los posibles subsets del metodo
for fila in hoja.iter_rows(min_col=1, max_col=1):
    celda = fila[0]
    if celda.value is not None:
        subsets.append(celda.value) 

#print("---------------")
subsets.pop(0)  # Elimino el elemento que contiene el nombre del método
subsets_a_mostrar = []
for subset in subsets:
    if st.toggle(subset):
        subsets_a_mostrar.append(subset)

# BLOQUE PRINCIPAL
# Leer cada fila por separado, con el vector subsets
if len(subsets_a_mostrar) != 0:
    vector_total = []
    for fila in subsets_a_mostrar:
        valores = obtener_rango_combinado_y_valores(hoja, fila)  # valores: lista con diccionarios
        # total_casos obtiene todas las columnas en donde tiene algoritmos (tupla para no repetir las columnas)
        total_casos = set({})   # Indica qué columnas tienen algs (la cantidad de casos del subset)
        for dato in valores:
            total_casos.add(dato['columna'])
        # Pasarlo a lista y ordenarlo alfabeticamente
        total_casos = list(total_casos)
        total_casos.sort()

        # Leer cada columna por separado, con el vector total_casos
        for columna in total_casos:
            # Quedarse con un solo algoritmo para un caso en especifico
            algs_un_caso = []
            for dato in valores:
                if dato['columna'] == columna:
                    algs_un_caso.append(dato['algoritmo'])
            numero = random.randint(0, len(algs_un_caso)-1)
            vector_total.append(algs_un_caso[numero])
    # Limpiar vector_total de caracteres nulos y espacios
    vector_total = list(filter(None, vector_total))
    vector_total = [x for x in vector_total if x != ' ']

    # Filtrar los elementos que tienen contenido real, si hay algo vacio se va
    vector_total = [x for x in vector_total if x.strip() != '']

    # Invertir todos los algoritmos, usando la funcion en el otro script
    invertido_total = []
    for algoritmo in vector_total:
        invertido_total.append(invertir_alg(algoritmo))

    numero = random.randint(0, len(invertido_total)-1)
    # Inicializar la variable en la sesión si no existe
    if "alg_random" not in st.session_state:
        st.session_state.alg_random = invertido_total[numero]

    # Botón para cambiar de algoritmo
    if st.button("Next alg"):
        st.session_state.alg_random = invertido_total[numero]

    # Mostrar el algoritmo seleccionado
    st.write(st.session_state.alg_random)

# Aclaraciones y demás
st.markdown("---")  # Línea divisoria
st.markdown(
    """
    **Notes**:
    - This does not generate any algorithm, it just takes the ones shown in this [drive](https://docs.google.com/spreadsheets/d/1OFXakCV85Mp2zsQBXMxiMX9a506JeAcLnUXZr8FgXAY/) and then reverse them.
    - If you do not press the Next alg button, the algorithm shown is not going to change, even if you change the method.
    """,
    unsafe_allow_html=True
)
