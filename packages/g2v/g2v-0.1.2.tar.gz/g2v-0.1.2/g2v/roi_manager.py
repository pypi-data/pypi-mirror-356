"""ROI selection and management for g2cubeviewer."""

import numpy as np
import pandas as pd
from typing import List


class ROIManager:
    """Class to manage region of interest selections."""

    def __init__(self, image_height: int, image_width: int):
        """
        Initialize the ROI manager.

        Args:
            image_height (int): Height of the image
            image_width (int): Width of the image
        """
        self.image_height = image_height
        self.image_width = image_width
        self.selections = []  # List of (g2_values, name, color)
        self.selection_rects = []  # List of (min_row, max_row, min_col, max_col)
        self.selection_colors = []  # List of colors for each selection
        self.current_selection = (0, 10, 0, 10)  # (min_row, max_row, min_col, max_col)
        self.selected_indices = []  # List of (row, col) tuples
        self.tau = None  # Time step for g2 calculation
        self.g2cube = None  # G2 correlation cube
        self.masks = []  # List of masks for each selection

    def update_current_selection(
        self, min_row: int, max_row: int, min_col: int, max_col: int
    ):
        """
        Update the current selection coordinates.

        Args:
            min_row (int): Minimum row index
            max_row (int): Maximum row index
            min_col (int): Minimum column index
            max_col (int): Maximum column index
        """
        self.current_selection = (min_row, max_row, min_col, max_col)
        self._update_selected_indices()

    def _update_selected_indices(self):
        """Update the list of selected pixel indices based on current selection."""
        min_row, max_row, min_col, max_col = self.current_selection
        selected_indices = []
        for r in range(int(min_row), int(max_row) + 1):
            for c in range(int(min_col), int(max_col) + 1):
                if (
                    0 <= r < self.image_height and 0 <= c < self.image_width
                ):
                    selected_indices.append((r, c))
        self.selected_indices = selected_indices

    def add_selection(self, g2_values: np.ndarray, name: str, color: str):
        """
        Add a new selection to the list.

        Args:
            g2_values (np.ndarray): Mean g2 values for the selection
            name (str): Name of the selection
            color (str): Color for the selection
        """
        self.selections.append((g2_values, name, color))
        self.selection_rects.append(self.current_selection)
        self.selection_colors.append(color)

    def clear_selections(self):
        """Clear all selections."""
        self.selections = []
        self.selection_rects = []
        self.selection_colors = []

    def get_selection_dataframe(self) -> pd.DataFrame:
        """
        Convert selections to a DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing selection information
        """
        roi_data = {
            "Selection": [],
            "Min Row": [],
            "Max Row": [],
            "Min Column": [],
            "Max Column": [],
        }
        for i, rect in enumerate(self.selection_rects):
            min_row, max_row, min_col, max_col = rect
            roi_data["Selection"].append(f"Selection {i + 1}")
            roi_data["Min Row"].append(min_row)
            roi_data["Max Row"].append(max_row)
            roi_data["Min Column"].append(min_col)
            roi_data["Max Column"].append(max_col)

        return pd.DataFrame(roi_data)

    def create_mask_from_indices(self, selected_indices: List) -> np.ndarray:
        """
        Create a mask from selected pixel indices.

        Args:
            selected_indices (list): List of (row, col) tuples for selected pixels
        Returns:
            np.ndarray: Mask array with selected pixels set to 1
        """
        mask = np.zeros((self.image_height, self.image_width), dtype=np.uint8)
        for r, c in selected_indices:
            if 0 <= r < self.image_height and 0 <= c < self.image_width:
                mask[r, c] = 1
        return mask

    def update_masks_from_selections(self) -> List:
        """
        Update masks for all selections based on selected indices.

        Returns:
            List: List of masks for each selection
        """
        self.masks = [
            self.create_mask_from_indices(self.selected_indices)
            for _ in range(len(self.selections))
        ]
        return self.masks
