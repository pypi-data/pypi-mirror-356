# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 17:00:52 2022

@author: pkiefer
"""
import emzed
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
from skl2onnx import to_onnx
import onnxruntime as ort
from ..utils import color_column_by_value

# from .peak_metrics import update_metrics  # , mv_imputation

"""
The path refers to a table of sample '2021121_0394_bemaier_B17_hilic_neg_neg_Leaf216_R2.mzML',
which was analyzed using emzed.run_festur_finder_metabo applying default settings defined
in 
emzed.ext.emzed2.basic_processing.ff_metabo_config.get_default_ff_metabo()
All peaks were manually scored  
0: not a peak, 
1:  critical peak (i.e. double peak, important tailing, low s/n, ...), 
2:  high quality peak
"""

# path= r'Z:\pkiefer\projects\apacheco\peaks_classification\RF_predictor_features.table'


def create_classifier(
    path, max_depth=3, score_col="true_positive", area_col="area_chromatogram"
):
    """
    creates a RandomForestClassifier object for peak peak scoring

    Parameters
    ----------
    path : emzed Table
        peak classification table with mandatory columns `area_col`,
        `zig_zag_index`, `gaussian similarity`, `max_apex_boundery_ratio`.
        to add peak metrics to table check
        -> target_workflow.scoring.update_peak_metrics
    max_depth : int, optional
        Max depth of random forest tree. The default is 3.
    score_col : name of emzed.Table.column, optional
        Contains user assigned quality score values ranging from
        0 (no peak) to 2 (high quality peak)
        The default is 'true_positive'.

    Returns
    -------
    sklearn.ensemble._forest.RandomForestClassifier

    """
    t = emzed.io.load_table(path)
    columns = [
        area_col,
        # 'no_spectra',
        # 'snr',
        "zigzag_index",
        "gaussian_similarity",
        "max_apex_boundery_ratio",
        "sharpness",
        "tpsar",
    ]
    data = np.array(list(zip(*[t[n] for n in columns])), dtype=np.float32)
    # column true positive contains
    # values == 0 > false red ,
    # values == 1 > critical, yellow,
    # values == 2 > good, green
    y = t[score_col].to_list()
    clf = RandomForestClassifier(100, max_depth=3)
    cv = ShuffleSplit(n_splits=25, test_size=0.3, random_state=0)
    scores = cross_val_score(clf, data, y, cv=cv)
    msg = f"cross validatiom score {scores.mean():.2f} +- {scores.std():.3f}"
    print(msg)
    clf.fit(data, y)
    # we convert the sklearn model into the onnx binary format
    model = to_onnx(clf, data[:1])
    return model


def score_peaks(t, path_to_classifier, min_spectra=6):
    class2color = {0: "#FF0000", 1: "#FFFF00", 2: "#00FF00"}
    # mv_imputation(t)
    t.add_enumeration("rid")
    classifiable, low_qual = split_by_spectra_count(t, min_spectra)
    data = _extract_classification_data(classifiable)
    # we replace infinity values by high numbers
    rid2score = {rid: 0 for rid in low_qual.rid}
    session = ort.InferenceSession(
        path_to_classifier, providers=["CPUExecutionProvider"]
    )
    input_name = session.get_inputs()[0].name
    label_name = session.get_outputs()[0].name
    scores = session.run([label_name], {input_name: data})[0]
    rid2score.update(dict(zip(classifiable.rid, scores)))
    t.add_or_replace_column(
        "peak_quality_score", t.apply(rid2score.get, t.rid), int, insert_after="id"
    )
    color_column_by_value(t, "peak_quality_score", class2color)
    t.drop_columns("rid")


# def color_column(t, colname, color_col):
#     if not "color" in t.col_names:
#         t.add_column_colname("color", [{}] * len(t), object, format_=None)

#     t.add_or_replace_column(
#         "color", t.apply(_update_color, colname, t[color_col], t.color)
#     )


# def _update_color(key, value, colname2color):
#     colname2color[key] = value
#     return colname2color


def split_by_spectra_count(t, min_spectra):
    classifiable = t.filter(t.no_spectra > min_spectra, keep_view=True)
    low_qual = t.filter(t.no_spectra <= min_spectra, keep_view=True)
    return classifiable, low_qual


def _extract_classification_data(t):
    columns = [
        "linear_model",
        "zigzag_index",
        "gaussian_similarity",
        "max_apex_boundery_ratio",
        "sharpness",
        "tpsar",
    ]
    df = t.extract_columns(*columns).to_pandas()
    # we extract area values from integration with linear model
    df.linear_model = [m.area for m in df.linear_model]
    # since we random forest predictor uses float32
    data = df.to_numpy(dtype=np.float32)
    data[np.isneginf(data)] = -1e38
    data[np.isinf(data)] = 1e38
    return data
