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
st.sidebar.image("figs/dsa_banner_dashboard.png")
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
tab_a, tab_b, tab_c = st.tabs(
    ["Predicción Modelo ML", "Exploración de Datos", "Contexto de negocio"]
)


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
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex de {column}",
                )
                if user_text_input:
                    df = df[df[column].tabr.contains(user_text_input)]

    return df


df = filter_dataframe(data)
########################## MOSTRAR DATOS ##########################

tab_b.write(df)


########################## HISTOGRAMA COLUMNA IZQUIERDA TAB B ##########################

hist_col = tab_b.selectbox(
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


tab_b.markdown(f"## Histograma de frecuencia variable **{hist_col}**")
tab_b.bar_chart(data=make_data_hist(hist_col), x=hist_col, y="Conteo", color="#19b1c7")


########################## PREGUNTAS ##########################


preguntas = [
    "Reconoce una amplia gama de técnicas para generar ideas",
    "Le es difícil construir, mejorar, analizar o evaluar sus propias ideas para mejorar su creatividad",
    "Es abierto y sensible a perspectivas nuevas y diversas; incorpora ideas y realiza retroalimentación grupal.",
    "Cuando falla, intenta olvidar lo sucedido y sigue adelante con lo que estaba trabajando",
    "Comprende los sistemas y estrategias para abordar  problemas desconocidos",
    "Utiliza varios tipos de razonamiento  (inductivo, deductivo, lógico, hipotético, transductivo, lingüístico,  etc.) de manera apropiada a cada situación",
    "Saca conclusiones que no están basadas en la interpretación ni el análisis de información.",
    "Cuando intenta identificar formas de resolver problemas se basa en lo conocido, evitando tomar riesgos.",
    "Aborda situaciones haciendo razonamientos desde distintas perspectivas y aproximaciones.",
    "Analiza y evalúa los diferentes componentes de una situación y el impacto que tienen en los resultados globales.",
    "Confía plenamente en la información que consulta y la aplica sin necesidad de verificarla.",
    "Hace preguntas significativas que evidencian varios puntos de vista y conduzcan a mejores soluciones",
    "Demuestra capacidad para trabajar respetuosamente con diversos equipos y valora las contribuciones individuales realizadas por cada miembro del equipo.",
    "Cuando trabaja en equipo usted se mantiene firme con sus ideas, defendiéndolas para cumplir sus objetivos.",
    "Respeta las diferencias culturales y trabaja efectivamente con personas de diversos orígenes sociales y culturales.",
    "Las personas externas difícilmente aportan a la innovación y calidad de un trabajo.",
    "Es consciente de varios tipos de interacción verbal (conversaciones, entrevistas, debates, etc.) y las principales características de diferentes estilos y registros en lenguaje hablado.",
    "En contextos complejos, sus comunicaciones no logran los objetivos y a veces son malinterpretadas.",
    "Cuando entrega un mensaje, hablado o escrito, cuenta con los suficientes argumentos para convencer a cualquier público",
    "Le cuesta trabajo dialogar de manera constructiva con personas que piensan muy diferente a usted",
]

preguntas_dict = {index + 1: value for index, value in enumerate(preguntas)}


preguntas_options = [f"p{i}: {preguntas_dict[i]}" for i in range(1, 21)]

preguntas_user = tab_b.multiselect(
    "Elige la(s) pregunta(s) de interés:",
    options=preguntas_options,
    placeholder="Elija al menos una opción",
    default=[
        preguntas_options[6],
        preguntas_options[11],
        preguntas_options[4],
        preguntas_options[14],
        preguntas_options[8],
        preguntas_options[1],
        preguntas_options[17],
        preguntas_options[19],
        preguntas_options[16],
        preguntas_options[5],
    ],
)
########################## CICLO PARA PRINT DE OPCIONES ##########################

col_1, col_2 = tab_b.columns(2)
for i, pregunta_user in enumerate(preguntas_user):
    if (
        1 + i
    ) % 2 == 0:  # para decidir si poner en columna 1 o 2 según si es par o impar el index
        col_for = col_2
    else:
        col_for = col_1

    col_for.markdown(f"#### {pregunta_user}")

    temp = pd.DataFrame(df[pregunta_user.split(":")[0]].copy())

    col_for.bar_chart(
        data=make_data_hist(
            pregunta_user.split(":")[0],
        ),
        x=pregunta_user.split(":")[0],
        y="Conteo",
        color=["#19b1c7"],
    )

######################################################################

########################## TAB C: CONTENIDO ##########################

######################################################################


tab_c.markdown(
    """
## Descripción de la información a usar:

En este proyecto, se recopilan datos anonimizados del instrumento de perfilación de competencias del siglo
XXI, suministrados por docentes y agentes educativos de instituciones educativas y centros de desarrollo
infantil en Colombia.
La base de datos consta de un total de 5270 registros de docentes, cada uno de los cuales incluye
información socio-demográfica, como género, grupo de edad, nivel educativo, posición laboral, región
geográfica, departamento, ubicación de la institución, fecha de cumplimentación del cuestionario y las
respuestas relacionadas con cada pregunta del instrumento. Además, se dispone de un archivo que contiene
la codificación de las preguntas, la competencia correspondiente y si la pregunta se encuentra invertida.
Todos los datos se encuentran en formato xlsx debido a que las respuestas se recopilan a través de
formularios en Google Forms. Este formato facilita la recopilación y el procesamiento de datos. Asegura la
accesibilidad y el intercambio de datos a largo plazo, y permite su respaldo y almacenamiento eficiente. Los
datos son propios del proyecto

## ¿Cómo se obtendrá la información?

Los datos son suministrados en formato .xlsx por la fundación Future Education (se mantiene confidencial
el nombre real de la empresa) se recolecta a través de formularios en línea creados utilizando la plataforma
Google Forms. Esta metodología proporciona un proceso estructurado y estandarizado para recopilar
respuestas de los docentes y agentes educativos.
La base de datos completa viene anonimizada para proteger la privacidad de los docentes y se podrán
realizar actualizaciones a solicitud a medida que se registren nuevas respuestas en el formulario.
La base de datos de dominios también es suministrada en formato .xlsx y permanece invariable a menos que
exista algún cambio en la metodología que será alertado por la empresa.

## Copyright, Intellectual Property Rights... ¿cómo se manejarán?

La información generada por este equipo de trabajo tiene exclusivamente fines académicos y será
compartida únicamente con los docentes y tutores del curso "Despliegue de Soluciones Analíticas".
Cualquier uso o divulgación adicional de esta información está estrictamente prohibido sin el
consentimiento expreso de Jesús Alberto Parada Pérez quien funge como co-owner y es el propietario de los
datos. Esta medida garantiza el respeto y la protección de los derechos de autor y la propiedad intelectual,
así como la preservación de la confidencialidad de la información.
Se tiene planeado la publicación de un repositorio público en la plataforma Github con el objetivo de
presentar los resultados y conclusiones del proyecto.

## ¿Que puede hacer este tablero?

1. Filtrar y explorar la información socio-demográfica, para ver relaciones de información en ese alcance
1. Filtrar y explorar información solo de respuestas, para observar patrones.
1. Interactuar con una API de ML asociada a un modelo dado.

"""
)
