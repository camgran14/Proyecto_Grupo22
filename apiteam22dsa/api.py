from typing import List

from fastapi import FastAPI

from classes import ModeloAPI, EntradaModelo, SalidaModelo

# Inicializar una aplicación FastAPI

app = FastAPI(
    title="API para Modelo de ML - Despliegue de Soluciones Analíticas", version="1.0.0"
)


# Definir un endpoint para el modelo de predicción


@app.post(
    "/predecir",
    response_model=List[SalidaModelo],
    tags=["API Predicción DSA - Grupo 22"],
)
async def predecir_score(entradas: List[EntradaModelo]):
    """
    Endpoint de la API encargado de predecir el score de los docentes de acuerdo a las preguntas seleccionadas.

    Parameters:
        - entradas: Lista de objetos EntradaModelo que representan las entradas del modelo.

    Returns:
        - Lista de objetos SalidaModelo con las predicciones de salida del modelo.
    """

    # Inicializar una lista para almacenar las respuestas del modelo

    respuesta = list()

    # Iterar sobre cada entrada en la lista de entradas
    for entrada in entradas:
        # Crear una instancia del modelo con las entradas actuales
        modelo = ModeloAPI(*entrada)
        # Realizar la predicción usando el modelo y agregarla a la lista de respuestas
        respuesta.append(modelo.predecir()[0])

    # Devolver la lista de respuestas
    return respuesta
