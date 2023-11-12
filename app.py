import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)


st.set_page_config(layout="wide")


########################## SIDEBAR ##########################

st.sidebar.title("Dashboard Proyecto  Team22")
st.sidebar.markdown(
    """
## Integrantes:
* Jorge Caballero
* Jesus Parada
* Camilo Grande
* Catalina Garcia
"""
)

########################## TABS ##########################
tab_a, tab_b = st.tabs(["Modelo ML", "Exploración de Datos"])


########################## COLS TAB A ##########################

col_a, col_b = tab_a.columns(2)

######################################################################

########################## TAB A: CONTENIDO ##########################

######################################################################


########################## CREAR PREGUNTAS ##########################


def create_question(column, question_text):
    return column.radio(
        label=question_text,
        options=["Nunca", "A veces", "Constantemente", "Siempre"],
    )


p7 = create_question(
    col_a,
    "Saca conclusiones que no están basadas en la interpretación ni el análisis de información.",
)
p12 = create_question(
    col_b,
    "Hace preguntas significativas que evidencian varios puntos de vista y conduzcan a mejores soluciones",
)
p5 = create_question(
    col_a, "Comprende los sistemas y estrategias para abordar  problemas desconocidos."
)
p15 = create_question(
    col_a,
    "Respeta las diferencias culturales y trabaja efectivamente con personas de diversos orígenes sociales y culturales.",
)
p9 = create_question(
    col_b,
    "Aborda situaciones haciendo razonamientos desde distintas perspectivas y aproximaciones.",
)
p2 = create_question(
    col_b,
    "Le es difícil construir, mejorar, analizar o evaluar sus propias ideas para mejorar su creatividad",
)
p18 = create_question(
    col_b,
    "En contextos complejos, sus comunicaciones no logran los objetivos y a veces son malinterpretadas.",
)
p20 = create_question(
    col_a,
    "Le cuesta trabajo dialogar de manera constructiva con personas que piensan muy diferente a usted",
)
p17 = create_question(
    col_a,
    "Es consciente de varios tipos de interacción verbal (conversaciones, entrevistas, debates, etc.) y las principales características de diferentes estilos y registros en lenguaje hablado.",
)
p6 = create_question(
    col_b,
    "Utiliza varios tipos de razonamiento  (inductivo, deductivo, lógico, hipotético, transductivo, lingüístico,  etc.) de manera apropiada a cada situación",
)


########################## DIVIDER ##########################

tab_a.divider()

########################## INTERACTION PREDICT BUTTON ##########################

_, button_div, _ = tab_a.columns([1, 5, 1])

predecir = button_div.button("Predecir", use_container_width=True)
if predecir:
    # TODO: Interacción con API y presentación de resultados modelo ML
    tab_a.divider()
    tab_a.markdown(
        "De acuerdo a sus respuestas, el nivel de desempeño general fue **ALTO** "
    )
    tab_a.markdown(
        "De acuerdo a su desempeño general, el siguiente contenido puede ser de interés cómo oportunidad de mejora:"
    )
    tab_a.markdown("[PLACEHOLDER]")

######################################################################

########################## TAB B: CONTENIDO ##########################

######################################################################


########################## CARGAR DATOS ##########################


@st.cache_data
def load_data():
    data_sc = pd.read_excel("data/Base perfilación de competencias_310823.xlsx")
    # Reemplazar los valores incorrectos con NaN
    data_sc["departamento"] = data_sc["departamento"].replace("NINGUNO", np.nan)
    data_sc["ubicacioninstitucion"] = data_sc["ubicacioninstitucion"].replace(
        "ninguna", np.nan
    )
    data_sc["edades"] = data_sc["edades"].replace(
        ["Entre 0 y 6 años", "Entre 7 y 14 años", "Entre 15 y 17 años"], np.nan
    )
    # Reemplazar los valores Mujer con mujer
    data_sc["sexoinscrito"] = data_sc["sexoinscrito"].replace("Mujer", "mujer")
    ## Imputar con la moda
    estrategia = "most_frequent"

    imp = SimpleImputer(missing_values=np.nan, strategy=estrategia)
    imp.fit(data_sc)
    # Imputar los valores faltantes en el DataFrame
    data_imputado = pd.DataFrame(imp.transform(data_sc), columns=data_sc.columns)
    # Mapear las respuestas a los valores numéricos
    mapeo_respuestas = {"Nunca": 1, "A veces": 2, "Constantemente": 3, "Siempre": 4}

    # Variables
    variables_p = [
        "p2",  # Creatividad e innovación
        "p5",
        "p6",
        "p7",  # Resolucion de problemas
        "p9",
        "p12",  # Pensamiento critico
        "p15",  # Trabajo colaborativo
        "p17",
        "p18",
        "p20",
    ]  # Comunicación

    # Aplicar el mapeo a las columnas correspondientes
    for variable in variables_p:
        data_imputado[variable] = data_imputado[variable].replace(mapeo_respuestas)
    # Variables que deben invertirse
    variables_invertir = ["p2", "p7", "p18", "p20"]

    # Invertir las respuestas en las columnas seleccionadas
    for variable in variables_invertir:
        data_imputado[variable] = (
            5 - data_imputado[variable]
        )  # esto "invierte" los valores

    data_imputado = data_imputado.rename(columns={"Year": "Año"})
    data_imputado["Año"] = data_imputado["Año"].astype(int)
    data_imputado["Mes"] = data_imputado["Mes"].astype(int)
    data_imputado["ID"] = data_imputado["ID"].astype(str)

    return data_imputado


data = load_data()
########################## FILTRAR DATOS ##########################


def filter_dataframe(df: pd.DataFrame, tab=tab_b) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns
    Adapted from https://github.com/tylerjrichards

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe


    """
    modify = tab.checkbox("Añadir Filtros")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = tab.container()

    with modification_container:
        to_filter_columns = tab.multiselect(
            "Filtrar DataFrame por", df.columns, placeholder="Elige una opción"
        )
        for column in to_filter_columns:
            left, right = tab.columns((1, 20))
            left.write("↳")
            # Treat columns with < 33 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 33:
                user_cat_input = right.multiselect(
                    f"Valores para {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                    placeholder="Elige al menos una opción",
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                tabep = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Valores para {column}",
                    _min,
                    _max,
                    (_min, _max),
                    tabep=tabep,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Valores para {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    tabart_date, end_date = user_date_input
                    df = df.loc[df[column].between(tabart_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex de {column}",
                )
                if user_text_input:
                    df = df[df[column].tabr.contains(user_text_input)]

    return df


df = filter_dataframe(
    data[
        [
            "ID",
            "Año",
            "Mes",
            "solucion",
            "regional",
            "departamento",
            "ubicacioninstitucion",
            "cargo",
            "edades",
            "formacion",
            "sexoinscrito",
            "Marca temporal",
            "formulario",
        ]
    ]
)
########################## MOSTRAR DATOS ##########################

tab_b.write(df)

########################## DISEÑO ##########################

col_1, col_2 = tab_b.columns(2)

########################## HISTOGRAMA COLUMNA IZQUIERDA TAB B ##########################

hist_col = col_1.selectbox(
    label="Elegir columna Histograma",
    options=[
        "Año",
        "Mes",
        "solucion",
        "regional",
        "departamento",
        "ubicacioninstitucion",
        "cargo",
        "edades",
        "formacion",
        "sexoinscrito",
    ],
)


def make_data_hist(column, data=df):
    data_fun = data.copy()
    data_fun["Conteo"] = 1
    return (
        pd.DataFrame(data_fun[[column, "Conteo"]].groupby(column).sum()["Conteo"])
        .reset_index()
        .sort_values(by="Conteo", ascending=False)
    )


col_1.markdown(f"## Histograma de frecuencia variable **{hist_col}**")
col_1.bar_chart(data=make_data_hist(hist_col), x=hist_col, y="Conteo")
