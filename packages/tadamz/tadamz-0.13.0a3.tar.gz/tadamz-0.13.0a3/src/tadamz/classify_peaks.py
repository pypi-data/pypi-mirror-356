# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 12:27:21 2023

@author: pkiefer
"""
from .scoring.peak_metrics import update_metrics
from .in_out import get_classifier_path
from .scoring.random_forest_peak_classification import score_peaks


def classify_peaks(table, kwargs):
    _classify_peaks(table, **kwargs)
    return table


def _classify_peaks(table, scoring_model, scoring_model_params, **kwargs):
    fun = globals()[scoring_model]
    fun(table, **scoring_model_params)


def random_forest_classification(
    table,
    classifier_name,
    ext=".predict",
    path_to_folder=None,
    ms_data_type="MS_Chromatogram",
    **kwargs
):
    classifier = get_classifier_path(classifier_name, path_to_folder=path_to_folder)
    # area_col = "area_chromatogram" if ms_data_type == "MS_Chromatogram" else "area"
    update_metrics(table, ms_data_type=ms_data_type)
    score_peaks(table, classifier)
