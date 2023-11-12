# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 14:02:53 2023

@author: camgr
"""

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

import warnings
warnings.filterwarnings("ignore")

#carga de datos
def cargar_datos(filename, nombre_base):
    data = pd.read_excel(f"data/{filename}")
    return data

data = cargar_datos("Base perfilación de competencias_310823.xlsx", "Base de datos:")    

#Mapoe Respuestas
# Mapear las respuestas a los valores numéricos
mapeo_respuestas = {
    "Nunca": 1,
    "A veces": 2,
    "Constantemente": 3,
    "Siempre": 4
}

# Variables
variables_p = ['p1', 'p2', 'p3', 'p4', #Creatividad e innovación
               'p5', 'p6', 'p7', 'p8', # Resolucion de problemas
               'p9', 'p10', 'p11', 'p12', # Pensamiento critico
               'p13', 'p14', 'p15', 'p16', # Trabajo colaborativo
               'p17', 'p18', 'p19', 'p20'] # Comunicación

# Aplicar el mapeo a las columnas correspondientes
for variable in variables_p:
    data[variable] = data[variable].replace(mapeo_respuestas)

# Variables que deben invertirse
variables_invertir = ["p2", "p4", "p7", "p8", "p11", "p14", "p16", "p18", "p20"]

# Invertir las respuestas en las columnas seleccionadas
for variable in variables_invertir:
    data[variable] = 5 - data[variable]  # esto "invierte" los alores

#Patrones
# Selecciona las columnas que contienen las respuestas de los docentes (p1 a p20)
respuestas = data.iloc[:, 13:33]

# Identifica respuestas constantes por docente
respuestas_constantes = respuestas.apply(pd.Series.nunique, axis=1) == 1

# Identifica patrones en zigzag por docente
patron_zigzag = ((respuestas.diff(axis=1).abs() == 1) & (respuestas.diff(axis=1).notnull())).all(axis=1)

# Marca 'Constante' en la columna 'Patron_Respuesta' si todas las respuestas son iguales
data.loc[respuestas_constantes, 'Patron_Respuesta'] = 'Constante'

# Marca 'Zigzag' en la columna 'Patron_Respuesta' si hay un patrón de zigzag en las respuestas
data.loc[patron_zigzag, 'Patron_Respuesta'] = 'Zigzag'

# Se eliminan estos patrones al no ser confiables
data = data[data['Patron_Respuesta'] != 'Constante']
data = data[data['Patron_Respuesta'] != 'Zigzag']

# Se elimina la columna temporal de patrones
data.drop("Patron_Respuesta",axis=1, inplace=True)


#Seleccion de componentes
#componentes a eliminar:
coldrops = ['p1', 'p3', 'p4', 'p8', 'p10', 'p11', 'p13', 'p14', 'p16', 'p19']

def select_comp(data):
    data_sc = data.drop(coldrops,axis=1)
    return data_sc

data_sc = select_comp(data)


#intervalos de respuestas
# Asegúrate de que 'Marca temporal' sea del tipo datetime, si no lo es, conviértela
data_sc['Marca temporal'] = pd.to_datetime(data_sc['Marca temporal'])

# Ordenar el DataFrame por 'ID' y 'Marca temporal'
data_sc = data_sc.sort_values(by=['ID', 'Marca temporal'])

# Identificar pruebas realizadas por el mismo docente con menos de 6 meses de diferencia
data_sc['Diferencia_meses'] = data_sc.groupby('ID')['Marca temporal'].diff().dt.days // 30

# Encuentra los índices de los registros que deben ser excluidos
indices_a_eliminar = data_sc[(data_sc['Diferencia_meses'].lt(4) & data_sc['Diferencia_meses'].ge(0))].index

# Elimina los registros identificados del DataFrame original
data_sc = data_sc.drop(indices_a_eliminar)

# Se elimina la columna temporal de diferencia de meses
data_sc.drop("Diferencia_meses",axis=1, inplace=True)



#eliminar, imputar y remplazar
# Eliminar missing
data_sc.dropna(inplace=True, subset = ["regional"])
# Reemplazar los valores incorrectos con NaN
data_sc["departamento"] = data_sc["departamento"].replace("NINGUNO", np.nan)
data_sc["ubicacioninstitucion"] = data_sc["ubicacioninstitucion"].replace("ninguna", np.nan)
data_sc["edades"] = data_sc["edades"].replace(
    ["Entre 0 y 6 años", "Entre 7 y 14 años", "Entre 15 y 17 años"], np.nan)
# Reemplazar los valores Mujer con mujer
data_sc["sexoinscrito"] = data_sc["sexoinscrito"].replace("Mujer", "mujer")

## Imputar con la moda
estrategia="most_frequent"
imp = SimpleImputer(missing_values=np.nan, strategy=estrategia)
#convertir datatime en float para no afectar el fit
data_sc['Marca temporal'] = data_sc['Marca temporal'].dt.strftime("%Y-%m-%d %H:%M:%S")
imp.fit(data_sc)
# Imputar los valores faltantes en el DataFrame
data_imputado = pd.DataFrame(imp.transform(data_sc), columns=data_sc.columns)


#Separar y almacenar datos
col_select=['p7', 'p12', 'p5', 'p15', 'p9', 'p2', 'p17', 'p18', 'p20', 'p6']
col_select2=['ID','p7', 'p12', 'p5', 'p15', 'p9', 'p2', 'p17', 'p18', 'p20', 'p6']
data_SE = data_imputado.drop(col_select,axis=1)
data_p = data_imputado[col_select2]

data_imputado.to_excel('data/BD_G22.xlsx')
data_p.to_excel('data/BD_G22_P.xlsx')
data_SE.to_excel('data/BD_G22_SE.xlsx')