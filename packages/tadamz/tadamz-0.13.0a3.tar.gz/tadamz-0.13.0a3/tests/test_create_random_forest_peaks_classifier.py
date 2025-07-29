# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 16:29:16 2023

@author: pkiefer
"""
import emzed
import os
import pytest
from src.tadamz import create_random_forest_peak_classifier as rfpc

here = os.path.abspath(os.path.dirname(__file__))
data_folder = os.path.join(here, "data")


@pytest.fixture
def _t():
    return emzed.to_table("x", [1, 2], int)


@pytest.fixture
def _path_to_table():
    return os.path.join(data_folder, "classification_table_chromatogram.table")


@pytest.fixture
def kwargs_chrom():
    d = {}
    d["classifier_name"] = "test_classifier"
    d["inspect"] = False
    d["path_to_table"] = os.path.join(
        data_folder, "classification_table_chromatogram.table"
    )
    d["path_to_folder"] = data_folder
    d["ms_data_type"] = "MS_Chromatogram"
    d["score_col"] = "peaks_quality_score"
    d["overwrite"] = True
    return d


@pytest.fixture
def kwargs_pm():
    d = {}
    d["classifier_name"] = "test_classifier"
    d["inspect"] = False
    d["path_to_table"] = os.path.join(data_folder, "classification_table_peakmap.table")
    d["path_to_folder"] = data_folder
    d["ms_data_type"] = "Spectra"
    d["score_col"] = "peaks_quality_score"
    d["overwrite"] = True
    return d


def test__update_score_column_0(_t):
    rfpc._update_score_column(_t, "score")
    is_ = _t.score.to_list()
    assert is_ == [0, 0]


def test__update_score_column_1(_t):
    _t.add_enumeration("score")
    rfpc._update_score_column(_t, "score")
    is_ = _t.score.to_list()
    assert is_ == [0, 1]


def test__get_table_0():
    with pytest.raises(AssertionError):
        rfpc._get_table(None, None)


def test__get_table_1(_t, _path_to_table):
    with pytest.raises(AssertionError):
        rfpc._get_table(_path_to_table, _t)


def test__get_table_2(_t):
    is_ = rfpc._get_table(None, _t)
    assert is_ == _t


def test__get_table_3(_path_to_table):
    is_ = rfpc._get_table(_path_to_table, None)
    assert isinstance(is_, emzed.Table)


def test_generate_peak_classifier_0(kwargs_chrom):
    path = os.path.join(data_folder, "test_classifier.onnx")
    if os.path.exists(path):
        os.remove(path)
    rfpc.generate_peak_classifier(**kwargs_chrom)
    assert os.path.exists(path)


def test_generate_peak_classifier_1(kwargs_pm):
    path = os.path.join(data_folder, "test_classifier.onnx")
    if os.path.exists(path):
        os.remove(path)
    rfpc.generate_peak_classifier(**kwargs_pm)
    assert os.path.exists(path)
