import numpy as np
import pandas as pd
import h5py
from io import BytesIO
from g2v.utils import (
    save_data_to_h5,
    load_data_from_h5,
    prepare_g2_data_for_export,
)


def test_save_data_to_h5():
    # Prepare test data
    roi_data = pd.DataFrame(
        {
            "Selection": ["Selection 1", "Selection 2"],
            "Min Row": [10, 20],
            "Max Row": [100, 200],
            "Min Column": [30, 40],
            "Max Column": [300, 400],
        }
    )

    g2_data = {
        "Index": [0, 1, 2, 3, 4],
        "Selection 1": [1.0, 1.1, 1.2, 1.3, 1.4],
        "Selection 2": [2.0, 2.1, 2.2, 2.3, 2.4],
    }

    tau = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    det_image = np.random.rand(10, 10)

    # Execute function
    result = save_data_to_h5(roi_data, g2_data, tau, det_image)

    # Verify results
    assert isinstance(result, BytesIO)

    # Check the content of the BytesIO by reading it back
    with h5py.File(result, "r") as h5file:
        # Check groups
        assert "ROI_Info" in h5file
        assert "g2_Curves" in h5file
        assert "Detector_Image" in h5file

        # Check ROI_Info datasets
        assert np.all(
            h5file["ROI_Info"]["Selection"][()]
            == np.array(roi_data["Selection"], dtype="S")
        )
        assert np.all(h5file["ROI_Info"]["Min_Row"][()] == roi_data["Min Row"])
        assert np.all(h5file["ROI_Info"]["Max_Row"][()] == roi_data["Max Row"])
        assert np.all(h5file["ROI_Info"]["Min_Column"][()] == roi_data["Min Column"])
        assert np.all(h5file["ROI_Info"]["Max_Column"][()] == roi_data["Max Column"])

        # Check g2_Curves datasets
        assert np.all(h5file["g2_Curves"]["Index"][()] == g2_data["Index"])
        assert np.all(h5file["g2_Curves"]["Selection 1"][()] == g2_data["Selection 1"])
        assert np.all(h5file["g2_Curves"]["Selection 2"][()] == g2_data["Selection 2"])
        assert np.all(h5file["g2_Curves"]["tau"][()] == tau)

        # Check Detector_Image dataset
        assert np.all(h5file["Detector_Image"]["Mean"][()] == det_image)


def test_save_data_to_h5_empty_data():
    # Test with minimal data
    roi_data = pd.DataFrame(
        {
            "Selection": [],
            "Min Row": [],
            "Max Row": [],
            "Min Column": [],
            "Max Column": [],
        }
    )

    g2_data = {"Index": []}

    tau = np.array([])
    det_image = np.zeros((0, 0))

    # Execute function
    result = save_data_to_h5(roi_data, g2_data, tau, det_image)

    # Verify results
    assert isinstance(result, BytesIO)

    # Check the content is valid HDF5
    with h5py.File(result, "r") as h5file:
        assert "ROI_Info" in h5file
        assert "g2_Curves" in h5file
        assert "Detector_Image" in h5file


def test_load_data_from_h5():
    # This function is not implemented yet (marked with TODO)
    # Just check it exists
    try:
        result = load_data_from_h5("dummy_file")
        assert result is None
    except NotImplementedError:
        # It's ok if it raises NotImplementedError
        pass


def test_prepare_g2_data_for_export_with_data():
    # Prepare test data
    values1 = np.array([1.0, 1.1, 1.2, 1.3, 1.4])
    values2 = np.array([2.0, 2.1, 2.2, 2.3, 2.4])
    selections = [(values1, "Selection 1", "red"), (values2, "Selection 2", "blue")]

    # Execute function
    result = prepare_g2_data_for_export(selections)

    # Verify results
    assert "Index" in result
    assert "Selection 1" in result
    assert "Selection 2" in result
    assert len(result["Index"]) == 5
    assert list(result["Index"]) == [0, 1, 2, 3, 4]
    assert np.all(result["Selection 1"] == values1)
    assert np.all(result["Selection 2"] == values2)


def test_prepare_g2_data_for_export_empty():
    # Test with empty selections
    selections = []

    # Execute function
    result = prepare_g2_data_for_export(selections)

    # Verify results
    assert "Index" in result
    assert len(result["Index"]) == 0


def test_prepare_g2_data_for_export_single_selection():
    # Test with a single selection
    values = np.array([1.0, 1.1, 1.2])
    selections = [(values, "Selection 1", "red")]

    # Execute function
    result = prepare_g2_data_for_export(selections)

    # Verify results
    assert "Index" in result
    assert "Selection 1" in result
    assert len(result.keys()) == 2  # Index and Selection 1
    assert list(result["Index"]) == [0, 1, 2]
    assert np.all(result["Selection 1"] == values)
