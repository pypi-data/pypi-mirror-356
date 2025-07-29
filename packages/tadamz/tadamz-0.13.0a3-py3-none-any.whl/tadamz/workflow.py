# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 09:56:27 2023

@author: pkiefer
"""

from .processing_steps import ProcessingSteps as _PS
from .processing_steps import PostProcessResult as _PPR

# suppress warnings in console output
import sys

if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")


def run_workflow(
    peaks_table,
    samples,
    config,
    calibration_table=None,
    sample_table=None,
    std_isotop_dist_table=None,
):
    """
    The config defines the sequence of processing steps
    and processing and the parameter settings of each step
    """
    wf = _PS(
        peaks_table,
        samples,
        config,
        calibration_table,
        sample_table,
        std_isotop_dist_table,
    )
    for step in wf.config["processing_steps"]:
        try:
            process = wf.__getattribute__(step)
        except AttributeError:
            print(
                f"""
                  WARNING
                  processing step `{step}` does not exist!
                  STEP will be skipped"""
            )
        process()
    return wf.result


def postprocess_result_table(
    result,
    config,
    postprocess_id=0,
    calibration_table=None,
    std_isotop_dist_table=None,
    process_only_tracked_changes=False,
):
    """


    Parameters
    ----------
    result : TYPE
        DESCRIPTION.
    config : TYPE
        DESCRIPTION.
    postprocess_id, int
     index of the posprocessing step listed in config

    Returns
    -------
    Table
        The processed result table

    """
    msg = f"{postprocess_id} exceeds number of postprocessings"
    assert postprocess_id < len(config["postprocessings"]), msg
    post = config["postprocessings"][postprocess_id]
    wf = _PPR(
        result,
        config,
        calibration_table,
        std_isotop_dist_table,
        process_only_tracked_changes,
    )
    for step in wf.config[post]:
        try:
            process = wf.__getattribute__(step)
        except AttributeError:
            print(
                f"""
                  WARNING
                  processing step `{step}` does not exist!
                  STEP will be skipped"""
            )
        if process_only_tracked_changes:
            msg = f"""{step} cannot be processed as tracked_change only since
            subset reprocessing is only possible when the step has already 
            been applied to the table. To apply {step} to the result table
            set `process_only_tracked_changes` to False. 
            """
            assert step in result.meta_data["applied_processing_steps"], msg
        process()
    wf.merge_reprocessed()
    return wf.result


def run_calibration(result_table, calibration_table, sample_table, config):
    return _PS.calibrate(result_table, calibration_table, sample_table, config)


# ___________________ test ___________________


def _test_workflow():
    peaks_table = ""
    samples = []
    config = _config()
    print(f"executed processing steps: {', '.join(config['processing_steps'])}")
    return run_workflow(peaks_table, samples, config)


def _config():
    config = {
        "extract_peaks": {},
        "classify_peaks": {},
        "normalize_peaks": {},
        "score_peaks": {},
        "processing_steps": [
            "extract_peaks",
            "classify_peaks",
            "normalize_peaks",
            "score_peaks",
            "undefined",
        ],
    }
    return config
