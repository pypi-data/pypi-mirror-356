# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 09:22:40 2023

@author: pkiefer
"""
import pytest
import emzed
import os
import numpy as np

# from src.targeted_wf import extract_peaks as ep
from src.tadamz import classify_peaks as cp
from src.tadamz.scoring import random_forest_peak_classification as rfc

here = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def kwargs():
    kwargs = {
        "scoring_model": "random_forest_classification",
        "scoring_model_params": {
            "classifier_name": "srm_peak_classifier",
            "ms_data_type": "MS_Chromatogram",
        },
    }
    return kwargs


@pytest.fixture
def table():
    spath = os.path.join(here, "data", "classification_table_chromatogram.table")
    t = emzed.io.load_table(spath)
    return t


@pytest.fixture
def table1():
    spath = os.path.join(here, "data", "classification_table_peakmap.table")
    t = emzed.io.load_table(spath)
    return t


@pytest.fixture
def kwargs1():
    kwargs = {
        "scoring_model": "random_forest_classification",
        "scoring_model_params": {
            "classifier_name": "uplc_MS1_QEx_peak_classifier",
            "ext": ".onnx",
            "ms_data_type": "Spectra",
            "path_to_folder": os.path.abspath(os.path.join(here, "data")),
        },
    }
    return kwargs


@pytest.fixture
def table2():
    spath = os.path.join(here, "data", "score_table1.table")
    t = emzed.io.load_table(spath)
    return t


@pytest.fixture
def tm():
    columns = [
        "linear_model",
        "zigzag_index",
        "gaussian_similarity",
        "max_apex_boundery_ratio",
        "sharpness",
        "tpsar",
    ]
    rows = [[PModel(1e4), 3e40, 0, 1e-50, -2, -2e40]]
    types = [object, float, float, float, float, float]
    return emzed.Table.create_table(columns, types, rows=rows)


def test_classify_peaks_0(table, kwargs, regtest):
    t = cp.classify_peaks(table, kwargs)
    t = t.extract_columns("id", "peak_quality_score").to_pandas()
    print(t.to_string(), file=regtest)


def test_classify_peaks_1(table1, kwargs1, regtest):
    t = cp.classify_peaks(table1, kwargs1)
    t = t.extract_columns("id", "peak_quality_score").to_pandas()
    print(t.to_string(), file=regtest)


def test_classify_peaks_2(table2, kwargs1, regtest):
    t = cp.classify_peaks(table2, kwargs1)
    t = t.extract_columns("id", "peak_quality_score").to_pandas()
    print(t.to_string(), file=regtest)


def test__extract_classification_data(tm):
    data = rfc._extract_classification_data(tm)[0]
    expected = np.array([1e4, 1.0e38, 0, 0, -2, -1.0e38], dtype=np.float32)
    is_ = abs(data - expected)
    print(is_)
    print(data)
    print(expected)
    assert np.all(is_ < 1e-30)


class PModel:
    def __init__(self, area):
        self.area = area
