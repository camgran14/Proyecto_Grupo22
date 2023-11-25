import pytest

import sys
import mock
from apiteam22dsa.classes import EntradaModelo, SalidaModelo, ModeloAPI


def test_imports():
    try:
        import pandas as pd

        assert True

    except ImportError:
        assert False

    try:
        import streamlit as st

        assert True

    except ImportError:
        assert False


import pandas as pd


def test_read_data():
    data = pd.read_excel("./data/Base perfilación de competencias_310823.xlsx")
    assert data is not None



def test_instanciar():
    test = ModeloAPI(
        "Nunca",
        "Siempre",
        "Nunca",
        "Nunca",
        "Siempre",
        "Nunca",
        "Nunca",
        "Nunca",
        "Nunca",
        "Nunca",
    )
    assert test.p12 == "Siempre"
    assert test.p6 == "Nunca"


def test_cargar_modelo():
    test = ModeloAPI(
        "Nunca",
        "Siempre",
        "Nunca",
        "Nunca",
        "Siempre",
        "Nunca",
        "Nunca",
        "Nunca",
        "Nunca",
        "Nunca",
    )
    test._cargar_modelo()


def test_instanciar_input():
    EntradaModelo(
        p7="Nunca",
        p12="Siempre",
        p5="Nunca",
        p15="Nunca",
        p9="Nunca",
        p2="Nunca",
        p17="Nunca",
        p18="Nunca",
        p20="Nunca",
        p6="Nunca",
    )


def test_predecir_and_dataclasses():
    test_data = EntradaModelo(
        p7="Nunca",
        p12="Siempre",
        p5="Nunca",
        p15="Nunca",
        p9="Nunca",
        p2="Nunca",
        p17="Nunca",
        p18="Nunca",
        p20="Nunca",
        p6="Nunca",
    )
    modelo = ModeloAPI(*test_data)
    SalidaModelo(score=modelo.predecir()[0]["score"])
