import pytest

import sys
import mock


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
