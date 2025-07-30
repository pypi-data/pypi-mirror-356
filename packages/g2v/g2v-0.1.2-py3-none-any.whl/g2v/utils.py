"""Utility functions for g2cubeviewer."""

import h5py
import numpy as np
import pandas as pd
from io import BytesIO
from typing import List, Tuple, Dict, Any


def save_data_to_h5(
    roi_data: pd.DataFrame,
    g2_data: Dict[str, Any],
    tau: np.ndarray,
    det_image: np.ndarray,
) -> BytesIO:
    """
    Save ROI and g2 data to an HDF5 file.

    Args:
        roi_data (pd.DataFrame): DataFrame with ROI information
        g2_data (Dict): Dictionary with g2 curve data
        det_image (np.ndarray): 2D array for the detector image (mean)
        tau (np.ndarray): List of delays for g2 curves

    Returns:
        BytesIO: BytesIO object containing the HDF5 file
    """
    output = BytesIO()
    with h5py.File(output, "w") as h5file:
        # Save ROI information
        roi_group = h5file.create_group("ROI_Info")
        roi_group.create_dataset(
            "Selection", data=np.array(roi_data["Selection"], dtype="S")
        )
        roi_group.create_dataset("Min_Row", data=roi_data["Min Row"])
        roi_group.create_dataset("Max_Row", data=roi_data["Max Row"])
        roi_group.create_dataset("Min_Column", data=roi_data["Min Column"])
        roi_group.create_dataset("Max_Column", data=roi_data["Max Column"])

        # Save g2 curves
        g2_group = h5file.create_group("g2_Curves")
        g2_group.create_dataset("Index", data=g2_data["Index"])
        for name, values in g2_data.items():
            if name != "Index":
                g2_group.create_dataset(name, data=values)
        # Save delay list
        g2_group.create_dataset("tau", data=tau)

        # Save detector image
        det_group = h5file.create_group("Detector_Image")
        det_group.create_dataset("Mean", data=det_image)

    # Reset the pointer to the beginning of the stream
    output.seek(0)
    return output


def load_data_from_h5(file):
    """
    Load data from an HDF5 file.

    Args:
        file: File object or path to HDF5 file

    Returns:
        tuple: (roi_data, g2_data) - DataFrames with ROI and g2 data
    """
    # TODO: Implement loading H5 files
    pass


def prepare_g2_data_for_export(
    selections: List[Tuple[np.ndarray, str, str]],
) -> Dict[str, Any]:
    """
    Prepare g2 data for export.

    Args:
        selections (List[Tuple]): List of (values, name, color) tuples

    Returns:
        Dict: Dictionary with g2 curve data
    """
    g2_data = {
        "Index": list(range(len(selections[0][0]))) if selections else [],
    }

    for values, name, _ in selections:
        g2_data[name] = values

    return g2_data
