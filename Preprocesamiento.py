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

#Seleccion de componentes
#componentes a eliminar:
coldrops = ['p1', 'p3', 'p4', 'p8', 'p10', 'p11', 'p13', 'p14', 'p16', 'p19']

def select_comp(data):
    data_sc = data.drop(coldrops,axis=1)
    return data_sc

data_sc = select_comp(data)


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
imp.fit(data_sc)
# Imputar los valores faltantes en el DataFrame
data_imputado = pd.DataFrame(imp.transform(data_sc), columns=data_sc.columns)

#Mapoe Respuestas
# Mapear las respuestas a los valores numéricos
mapeo_respuestas = {
    "Nunca": 1,
    "A veces": 2,
    "Constantemente": 3,
    "Siempre": 4
}
# Variables
variables_p = ['p2', #Creatividad e innovación
               'p5', 'p6', 'p7', # Resolucion de problemas
               'p9', 'p12', # Pensamiento critico
               'p15', # Trabajo colaborativo
               'p17', 'p18', 'p20'] # Comunicación

# Aplicar el mapeo a las columnas correspondientes
for variable in variables_p:
    data_imputado[variable] = data_imputado[variable].replace(mapeo_respuestas)

# Variables que deben invertirse
variables_invertir = ["p2", "p7", "p18", "p20"]
# Invertir las respuestas en las columnas seleccionadas
for variable in variables_invertir:
    data_imputado[variable] = 5 - data_imputado[variable]  # esto "invierte" los alores

#Separar y almacenar datos
col_select=['p7', 'p12', 'p5', 'p15', 'p9', 'p2', 'p17', 'p18', 'p20', 'p6']
col_select2=['ID','p7', 'p12', 'p5', 'p15', 'p9', 'p2', 'p17', 'p18', 'p20', 'p6']
data_SE = data_imputado.drop(col_select,axis=1)
data_p = data_imputado[col_select2]

data_imputado.to_excel('data/BD_G22.xlsx')
data_p.to_excel('data/BD_G22_P.xlsx')
data_SE.to_excel('data/BD_G22_SE.xlsx')