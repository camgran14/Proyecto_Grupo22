"""
Este código define una estructura para un modelo de API utilizando la biblioteca Pydantic para la validación y documentación de datos de entrada y salida. A continuación, se presenta una documentación detallada para cada parte del código:

Clase EntradaModelo:
Esta clase hereda de BaseModel de Pydantic y define las entradas del modelo. Cada variable (p7, p12, ..., p6) tiene un tipo Literal con opciones predefinidas ("Nunca", "A veces", "Constantemente", "Siempre"). También se incluye una descripción para cada campo utilizando el atributo description de Pydantic.

Clase SalidaModelo:
Esta clase también hereda de BaseModel de Pydantic y define la salida del modelo. La variable score es de tipo float. Se proporciona un ejemplo usando el atributo example y se define un esquema adicional usando schema_extra.

Clase ModeloAPI:
Esta clase es responsable de cargar el modelo y realizar predicciones. Al inicializarse, toma los valores de entrada y los asigna a variables correspondientes. El método _cargar_modelo carga el modelo desde un archivo (ModeloAPI.pkl). El método _preprocesar_datos convierte las respuestas categóricas en valores numéricos y crea un DataFrame con estos valores para realizar la predicción. El método predecir carga el modelo, realiza el preprocesamiento y devuelve las predicciones en formato de diccionario.

Uso del Código:
EntradaModelo: Se utiliza para validar y documentar las entradas del modelo.
SalidaModelo: Se utiliza para validar y documentar la salida del modelo.
ModeloAPI: Se utiliza para interactuar con el modelo, cargarlo, preprocesar datos y realizar predicciones.
"""


from pydantic import BaseModel as BM
from pydantic import Field
from typing import Literal
import joblib
import pandas as pd


class EntradaModelo(BM):
    """
    Clase que define las entradas del modelo
    Configuración:
        - model_config: Configuración adicional para el modelo, que incluye ejemplos en formato JSON Schema.
    """

    p7: Literal["Nunca", "A veces", "Constantemente", "Siempre"] = Field(
        description="Respuesta Pregunta 7"
    )
    p12: Literal["Nunca", "A veces", "Constantemente", "Siempre"] = Field(
        description="Respuesta Pregunta 12"
    )
    p5: Literal["Nunca", "A veces", "Constantemente", "Siempre"] = Field(
        description="Respuesta Pregunta 5"
    )
    p15: Literal["Nunca", "A veces", "Constantemente", "Siempre"] = Field(
        description="Respuesta Pregunta 15"
    )
    p9: Literal["Nunca", "A veces", "Constantemente", "Siempre"] = Field(
        description="Respuesta Pregunta 9"
    )
    p2: Literal["Nunca", "A veces", "Constantemente", "Siempre"] = Field(
        description="Respuesta Pregunta 2"
    )
    p17: Literal["Nunca", "A veces", "Constantemente", "Siempre"] = Field(
        description="Respuesta Pregunta 17"
    )
    p18: Literal["Nunca", "A veces", "Constantemente", "Siempre"] = Field(
        description="Respuesta Pregunta 18"
    )
    p20: Literal["Nunca", "A veces", "Constantemente", "Siempre"] = Field(
        description="Respuesta Pregunta 20"
    )
    p6: Literal["Nunca", "A veces", "Constantemente", "Siempre"] = Field(
        description="Respuesta Pregunta 6"
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "p7": "Constantemente",
                    "p12": "Constantemente",
                    "p5": "Constantemente",
                    "p15": "Siempre",
                    "p9": "Siempre",
                    "p2": "Constantemente",
                    "p17": "Siempre",
                    "p18": "Siempre",
                    "p20": "Siempre",
                    "p6": "Constantemente",
                }
            ]
        }
    }


class SalidaModelo(BM):
    """
    Clase que controla que la salida si tenga sentido
    """

    score: float = Field(ge=-5, le=5, example=0.42)

    class Config:
        schema_extra = {"example": {"score": 0.42}}


class ModeloAPI:
    """
    Clase que gestiona la interacción con el modelo.

    Métodos:
        - __init__: Inicializa la clase con los valores de entrada.
        - _cargar_modelo: Carga el modelo desde un archivo.
        - _preprocesar_datos: Realiza el preprocesamiento de datos antes de la predicción.
        - predecir: Realiza la predicción utilizando el modelo cargado y los datos procesados
    """

    def __init__(self, *valores):
        variable_names = [
            "p7",
            "p12",
            "p5",
            "p15",
            "p9",
            "p2",
            "p17",
            "p18",
            "p20",
            "p6",
        ]
        for i, valor in enumerate(valores):
            # Asignar cada valor a self usando setattr
            setattr(self, variable_names[i], valor)

    def _cargar_modelo(self):
        """Carga el modelo desde un archivo."""

        self.modelo = joblib.load("ModeloAPI.pkl")

    def _preprocesar_datos(self):
        """Realiza el preprocesamiento de datos antes de la predicción."""

        valores = ["p7", "p12", "p5", "p15", "p9", "p2", "p17", "p18", "p20", "p6"]
        variables = []
        for valor in valores:
            variables.append(getattr(self, valor)[1])
            print(getattr(self, valor))
        mapeo_respuestas = {"Nunca": 1, "A veces": 2, "Constantemente": 3, "Siempre": 4}
        p7, p12, p5, p15, p9, p2, p17, p18, p20, p6 = [
            mapeo_respuestas[x] for x in variables
        ]

        p2, p7, p18, p20 = [5 - x for x in [p2, p7, p18, p20]]

        return pd.DataFrame(
            columns=["p7", "p12", "p5", "p15", "p9", "p2", "p17", "p18", "p20", "p6"],
            data=[[p7, p12, p5, p15, p9, p2, p17, p18, p20, p6]],
        )

    def predecir(self):
        """Realiza la predicción utilizando el modelo cargado y los datos procesados."""

        self._cargar_modelo()
        x = self._preprocesar_datos()
        y_pred = pd.DataFrame(self.modelo.predict(x)).rename(columns={0: "score"})
        return y_pred.to_dict(orient="records")
