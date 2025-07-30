"""Data generation and processing functions for g2cubeviewer."""

import numpy as np
import streamlit as st


@st.cache_data
def generate_pattern():
    """
    Generate a sample 3D data pattern with Gaussian curves.

    Returns:
        np.ndarray: Generated 3D array of shape (1000, 100, 100)
    """
    # Create the base array with random noise
    tau_len = 100
    shape = (tau_len, 200, 200)
    array = np.random.random(shape)  # Start with random noise everywhere

    # Create Gaussian curves along the first dimension
    x = np.linspace(-3, 3, tau_len)
    gaussian = np.exp(-0.1 * x**2)
    gaussian4 = np.exp(-1 * x**2)
    gaussian6 = np.exp(-2 * x**2)

    # Create correlated patterns in the 8x8 regions
    for i in range(tau_len):
        # Create gaussian pattern in first region
        array[i, 20:35, :25] = 5 * gaussian[i] * np.ones((15, 25))
        # Create gaussian pattern in second region
        array[i, 55:75, :25] = 5 * gaussian4[i] * np.ones((20, 25))
        # Create gaussian pattern in third region
        array[i, 35:50, :25] = 5 * gaussian6[i] * np.ones((15, 25))
        # Create gaussian pattern in first region
        array[i, :20, 25:50] = 5 * gaussian4[i] * np.ones((20, 25))
        # Create gaussian pattern in second region
        array[i, 20:35, 40:65] = 5 * gaussian6[i] * np.ones((15, 25))
        # Create gaussian pattern in third region
        array[i, 35:50, 70:95] = 5 * gaussian[i] * np.ones((15, 25))
    return array


def calculate_g2(img_stack: np.ndarray) -> np.ndarray:
    """
    Calculate the g2 correlation from an image stack using FFT method.

    Args:
        img_stack (np.ndarray): Input 3D array of shape (time, height, width)

    Returns:
        np.ndarray: G2 correlation matrix
    """
    # This is an fft-based method for calculating the correlation. It scales
    # like n log(n) instead of n**2, so it is far far faster at large n.
    # Calculating the numerators via FFT
    img_stack_padded = np.concatenate([img_stack, np.zeros_like(img_stack)], axis=0)
    img_stack_fft = np.fft.fft(img_stack_padded, axis=0)
    numerator_base = np.fft.ifft(img_stack_fft * img_stack_fft.conj(), axis=0)[
        : img_stack.shape[0]
    ].real
    n_elements = (np.arange(img_stack.shape[0]) + 1)[::-1]
    numerator_base /= n_elements[:, None, None]

    # This is just an efficient way to calculate the denominator
    # Calculating the denominators
    lcumsum = np.roll(np.cumsum(img_stack, axis=0), 1, axis=0)
    lcumsum[0, :, :] = 0
    rcumsum = np.roll(np.cumsum(img_stack[::-1], axis=0), 1, axis=0)
    rcumsum[0, :, :] = 0
    denominator_base = (2 * np.sum(img_stack, axis=0)) - lcumsum - rcumsum
    n_elements = 2 * img_stack.shape[0] - 2 * np.arange(img_stack.shape[0])
    denominator_base /= n_elements[:, None, None]

    # And we have our result!
    result = numerator_base / denominator_base**2
    len_result = result.shape[0]
    return result[1 : int(len_result // 2), :, :]  # Remove the first element (tau=0)


def get_mean_g2_for_roi(g2cube, selected_indices):
    """
    Calculate the mean g2 values for a selected region of interest.

    Args:
        g2cube (np.ndarray): G2 correlation array
        selected_indices (list): List of (row, col) tuples for selected pixels

    Returns:
        np.ndarray: Mean g2 values across selected pixels
    """
    if not selected_indices:
        return None

    selected_values = np.array([g2cube[:, r, c] for r, c in selected_indices])
    return np.mean(selected_values, axis=0)


def make_test_h5file(filename="test.h5"):
    """
    Create a highly compressed test HDF5 file with dummy data.

    Args:
        filename (str): Name of the file to save the HDF5 data.

    Returns:
        str: Path to the created file
    """
    import h5py
    import numpy as np

    # Use float16 for extreme size reduction - reduce precision by 75% compared to float64
    dtype = np.float16

    # Generate data at float16 precision (half the size of float32)
    mean_detector_image = np.random.rand(2048, 2048).astype(dtype)
    center_x, center_y = 1024, 1024
    x, y = np.meshgrid(np.arange(2048), np.arange(2048))
    gaussian_center = np.exp(
        -((x - center_x) ** 2 + (y - center_y) ** 2) / (2 * (300**2))
    ).astype(dtype)
    mean_detector_image += 5 * gaussian_center

    # Lower precision for the g2 cube data as well
    compressed_g2cube = np.random.rand(5, 2048, 2048).astype(dtype)

    # random boolean mask to simulate dead pixel or more advanced masking
    mask = np.random.rand(2048, 2048) > 0.1

    # Tau values likely need at least float32 for accuracy in logarithmic spacing
    tau_log = np.logspace(0, 3, num=5).astype(np.float32)
    tau_unit = "s"

    # Create a highly optimized HDF5 file
    with h5py.File(filename, "w") as f:
        # Configure compression settings for maximum savings
        compression_kwargs = {
            "compression": "gzip",
            "compression_opts": 9,  # Maximum compression level
            "shuffle": True,  # Byte shuffle filter improves compression
            "fletcher32": True,  # Adds checksum but helps with compression
        }

        # Optimize chunk size for compression efficiency
        # Use smaller chunks for better compression
        f.create_dataset(
            "g2_Curves",
            data=compressed_g2cube,
            chunks=(5, 256, 256),  # Chunk size optimized for compression
            **compression_kwargs,
        )

        f.create_dataset(
            "Detector_Image",
            data=mean_detector_image,
            chunks=(256, 256),  # Chunk size optimized for compression
            **compression_kwargs,
        )
        f.create_dataset(
            "Mask",
            data=mask,
            chunks=(256, 256),  # Chunk size optimized for compression
            **compression_kwargs,
        )

        # Even small datasets can be compressed
        f.create_dataset("tau_log", data=tau_log, **compression_kwargs)

        # Store tau_unit as an attribute instead of a dataset - saves overhead
        f.attrs["tau_unit"] = tau_unit

        # Set HDF5 file-level options for better compression
        f.attrs["VERSION"] = "1.0"  # Version tracking
        f.attrs["FILTERS_USED"] = "gzip, shuffle"  # Document filters used

    return filename


def h5_file_checks(file):
    """
    Perform checks on the HDF5 file to ensure it contains the required datasets.

    Args:
        file: File object or path to HDF5 file

    Returns:
        bool: True if all checks pass, False otherwise
    """
    import h5py

    with h5py.File(file, "r") as f:
        # Check for required datasets
        required_datasets = ["g2_Curves", "Detector_Image", "tau_log"]
        for dataset in required_datasets:
            if dataset not in f:
                st.error(f"Missing dataset: {dataset}")
                return False

        # Check for correct data types
        if not isinstance(f["g2_Curves"], h5py.Dataset):
            st.error("g2_Curves is not a dataset")
            return False
        if not isinstance(f["Detector_Image"], h5py.Dataset):
            st.error("Detector_Image is not a dataset")
            return False
        if not isinstance(f["tau_log"], h5py.Dataset):
            st.error("tau_log is not a dataset")
            return False
        # Check for correct shapes
        if f["g2_Curves"].ndim != 3:
            st.error("g2_Curves should be a 3D dataset")
            return False
        if f["Detector_Image"].ndim != 2:
            st.error("Detector_Image should be a 2D dataset")
            return False
        if f["tau_log"].ndim != 1:
            st.error("tau_log should be a 1D dataset")
            return False
        # check if tau_log and g2_Curves have the same length
        if f["g2_Curves"].shape[0] != f["tau_log"].shape[0]:
            st.error("g2_Curves and tau_log should have the same length")
            return False
        # check if g2_Curves and Detector_Image have the same shape
        if f["g2_Curves"].shape[1:] != f["Detector_Image"].shape:
            st.error(
                "g2_Curves and Detector_Image should have the same shape (height, width)"
            )
            return False
    return True
