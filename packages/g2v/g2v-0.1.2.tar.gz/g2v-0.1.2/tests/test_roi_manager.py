import numpy as np
import pandas as pd
from typing import List, Tuple

from g2v.roi_manager import ROIManager


def test_init():
    manager = ROIManager(100, 100)
    assert manager.image_height == 100
    assert manager.image_width == 100
    assert manager.current_selection == (0, 10, 0, 10)
    assert len(manager.selections) == 0
    assert len(manager.selected_indices) == 0
    assert manager.tau is None


def test_update_current_selection_valid():
    manager = ROIManager(10, 10)
    manager.update_current_selection(2, 5, 3, 7)
    assert manager.current_selection == (2, 5, 3, 7)
    selected = manager.selected_indices
    rows = [r for r, c in selected]
    cols = [c for r, c in selected]
    assert min(rows) == 2
    assert max(rows) == 5
    assert min(cols) == 3
    assert max(cols) == 7
    assert len(selected) == 20


def test_update_current_selection_min_row_gt_max_row():
    manager = ROIManager(10, 10)
    manager.update_current_selection(5, 2, 3, 7)
    assert manager.current_selection == (5, 2, 3, 7)
    assert len(manager.selected_indices) == 0
    assert isinstance(manager.selected_indices, List)
    assert isinstance(manager.selections, List) and all(
        isinstance(sel, Tuple)
        and len(sel) == 3
        and isinstance(sel[0], np.ndarray)
        and isinstance(sel[1], str)
        and isinstance(sel[2], str)
        for sel in manager.selections
    )


def test_update_current_selection_negative_min_row():
    manager = ROIManager(10, 10)
    manager.update_current_selection(-1, 5, 3, 7)
    selected = manager.selected_indices
    rows = [r for r, c in selected]
    assert min(rows) == 0
    assert max(rows) == 5
    cols = [c for r, c in selected]
    assert min(cols) == 3
    assert max(cols) == 7
    assert len(selected) == 30


def test_update_current_selection_max_row_beyond_image():
    manager = ROIManager(5, 10)
    manager.update_current_selection(2, 10, 3, 7)
    selected = manager.selected_indices
    rows = [r for r, c in selected]
    assert max(rows) == 4
    cols = [c for r, c in selected]
    assert min(cols) == 3
    assert max(cols) == 7
    assert len(selected) == 15


def test_add_selection():
    manager = ROIManager(10, 10)
    g2 = np.array([0.5, 0.6])
    manager.add_selection(g2, "Test", "red")
    assert len(manager.selections) == 1
    rect = manager.selection_rects[0]
    assert rect == (0, 10, 0, 10)
    manager.update_current_selection(2, 5, 3, 7)
    g2_2 = np.array([0.7, 0.8])
    manager.add_selection(g2_2, "Test2", "blue")
    assert len(manager.selections) == 2
    rect2 = manager.selection_rects[1]
    assert rect2 == (2, 5, 3, 7)


def test_clear_selections():
    manager = ROIManager(10, 10)
    manager.add_selection(np.array([1]), "A", "green")
    manager.add_selection(np.array([2]), "B", "yellow")
    assert len(manager.selections) == 2
    manager.clear_selections()
    assert len(manager.selections) == 0
    assert len(manager.selection_rects) == 0
    assert len(manager.selection_colors) == 0


def test_get_selection_dataframe():
    manager = ROIManager(10, 10)
    manager.update_current_selection(2, 5, 3, 7)
    manager.add_selection(np.array([1]), "Sel1", "red")
    manager.update_current_selection(6, 8, 4, 6)
    manager.add_selection(np.array([2]), "Sel2", "blue")
    df = manager.get_selection_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert df.columns.tolist() == [
        "Selection",
        "Min Row",
        "Max Row",
        "Min Column",
        "Max Column",
    ]
    assert df.iloc[0]["Selection"] == "Selection 1"
    assert df.iloc[0]["Min Row"] == 2
    assert df.iloc[0]["Max Row"] == 5
    assert df.iloc[0]["Min Column"] == 3
    assert df.iloc[0]["Max Column"] == 7
    assert df.iloc[1]["Selection"] == "Selection 2"
    assert df.iloc[1]["Min Row"] == 6
    assert df.iloc[1]["Max Row"] == 8
    assert df.iloc[1]["Min Column"] == 4
    assert df.iloc[1]["Max Column"] == 6


def test_get_selection_dataframe_empty():
    manager = ROIManager(10, 10)
    df = manager.get_selection_dataframe()
    assert df.empty


def test_single_row_column():
    manager = ROIManager(10, 10)
    manager.update_current_selection(3, 3, 4, 4)
    selected = manager.selected_indices
    assert len(selected) == 1
    assert selected[0] == (3, 4)


def test_zero_sized_selection():
    manager = ROIManager(10, 10)
    manager.update_current_selection(5, 2, 3, 7)
    assert len(manager.selected_indices) == 0


def test_add_selection_empty_g2():
    manager = ROIManager(10, 10)
    g2 = np.array([])
    manager.add_selection(g2, "Empty", "black")
    assert len(manager.selections) == 1
    assert len(manager.selection_rects) == 1


def test_create_mask_from_indices_empty():
    manager = ROIManager(10, 10)
    mask = manager.create_mask_from_indices([])
    assert np.sum(mask) == 0  # Mask should be all zeros
    assert mask.shape == (10, 10)
    assert mask.dtype == np.uint8


def test_create_mask_from_indices_single():
    manager = ROIManager(10, 10)
    mask = manager.create_mask_from_indices([(5, 5)])
    assert np.sum(mask) == 1  # Exactly one pixel should be set
    assert mask[5, 5] == 1
    assert mask.shape == (10, 10)


def test_create_mask_from_indices_multiple():
    manager = ROIManager(10, 10)
    indices = [(1, 2), (3, 4), (5, 6)]
    mask = manager.create_mask_from_indices(indices)
    assert np.sum(mask) == 3  # Three pixels should be set
    for r, c in indices:
        assert mask[r, c] == 1
    assert mask.shape == (10, 10)


def test_create_mask_from_indices_out_of_bounds():
    manager = ROIManager(5, 5)
    indices = [(1, 2), (6, 3), (3, 7), (-1, 2)]  # Some indices are out of bounds
    mask = manager.create_mask_from_indices(indices)
    assert np.sum(mask) == 1  # Only one pixel is within bounds
    assert mask[1, 2] == 1
    assert mask.shape == (5, 5)


def test_update_masks_from_selections_empty():
    manager = ROIManager(10, 10)
    masks = manager.update_masks_from_selections()
    assert len(masks) == 0
    assert len(manager.masks) == 0


def test_update_masks_from_selections_single():
    manager = ROIManager(10, 10)
    manager.update_current_selection(2, 4, 3, 5)  # Creates some selected indices
    manager.add_selection(np.array([0.5]), "Test", "red")
    masks = manager.update_masks_from_selections()
    assert len(masks) == 1
    assert np.sum(masks[0]) == len(manager.selected_indices)
    assert masks[0].shape == (10, 10)


def test_update_masks_from_selections_multiple():
    manager = ROIManager(10, 10)
    manager.update_current_selection(2, 4, 3, 5)  # Creates some selected indices
    manager.add_selection(np.array([0.5]), "Test1", "red")
    manager.add_selection(np.array([0.6]), "Test2", "blue")
    masks = manager.update_masks_from_selections()
    assert len(masks) == 2
    # Both masks should be identical since they're based on the same selected_indices
    assert np.array_equal(masks[0], masks[1])
    assert np.sum(masks[0]) == len(manager.selected_indices)
    assert masks[0].shape == (10, 10)
