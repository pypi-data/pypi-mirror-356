import plotly.graph_objects as go
import numpy as np
from typing import List, Tuple, Optional, Union
import streamlit as st


def downsample_image(image_data: np.ndarray, factor: int) -> np.ndarray:
    """
    Downsample the image data by a given factor.

    Args:
        image_data (np.ndarray): 2D array for the heatmap
        factor (int): Downsampling factor

    Returns:
        np.ndarray: Downsampled image data
    """
    if factor <= 1:
        return image_data
    return image_data[::factor, ::factor]


def create_heatmap_with_selections(
    image_data: np.ndarray,
    selection_rects: List[Tuple[int, int, int, int]],
    selection_colors: List[str],
    current_selection: Tuple[int, int, int, int],
    color_scale_min: Optional[float] = None,
    color_scale_max: Optional[float] = None,
    zoom_region: Optional[Tuple[int, int, int, int]] = None,
    select_colormap: Optional[str] = "Greys",
    factor: int = 1,
):
    """
    Create a heatmap with selection rectangles.

    Args:
        image_data (np.ndarray): 2D array for the heatmap
        selection_rects (List[Tuple]): List of selection rectangles
        selection_colors (List[str]): List of colors for each selection
        current_selection (Tuple): Current selection rectangle
        color_scale_min (float, optional): Minimum value for color scale
        color_scale_max (float, optional): Maximum value for color scale
        zoom_region (Tuple, optional): Region to zoom to (x0, x1, y0, y1)
        select_colormap (str, optional): Colormap for the heatmap
        factor (int): Downsampling factor for the image

    Returns:
        plotly.graph_objects.Figure: Plotly figure with heatmap and selections
    """

    image_data = downsample_image(image_data, factor)
    ds_rows, ds_cols = image_data.shape

    x_coords = np.arange(ds_cols) * factor + factor / 2 - 0.5
    y_coords = np.arange(ds_rows) * factor + factor / 2 - 0.5

    fig = go.Figure(
        data=go.Heatmap(
            z=image_data,
            x=x_coords,
            y=y_coords,
            colorscale=select_colormap,
            zmin=color_scale_min,
            zmax=color_scale_max,
            colorbar=dict(
                thickness=10,
                len=0.8,
                x=1.02,
                y=0.5,
            ),
        )
    )

    # Add shapes for all previous selections
    for i, rect in enumerate(selection_rects):
        min_row, max_row, min_col, max_col = rect
        color = selection_colors[i]

        # Add rectangle with increased transparency
        fig.add_shape(
            type="rect",
            x0=min_col - 0.5,
            y0=min_row - 0.5,
            x1=max_col + 0.5,
            y1=max_row + 0.5,
            line=dict(color=color, width=2),
            fillcolor="rgba(0, 0, 0, 0.0)",
        )

        # Add label for the selection
        fig.add_annotation(
            x=min_col,
            y=min_row,
            text=f"S {i + 1}",
            showarrow=False,
            arrowhead=1,
            ax=20,
            ay=-30,
            font=dict(color="white", size=12),
            bgcolor=color.replace("1.0", "0.1"),
            bordercolor=color.replace("1.0", "1.0"),
            borderwidth=2,
            borderpad=4,
        )

    # Add current selection
    min_row, max_row, min_col, max_col = current_selection

    # Add rectangle for current selection
    fig.add_shape(
        type="rect",
        x0=min_col - 0.5,
        y0=min_row - 0.5,
        x1=max_col + 0.5,
        y1=max_row + 0.5,
        line=dict(color="rgba(0, 255, 0, 0.8)", width=2),
        fillcolor="rgba(0, 0, 0, 0.0)",
    )

    # Add label for current selection
    fig.add_annotation(
        x=min_col,
        y=min_row,
        text="Current",
        showarrow=False,
        ax=20,
        ay=-30,
        font=dict(color="white", size=12),
        bgcolor="rgba(0, 255, 0, 0.1)",
        bordercolor="green",
        borderwidth=2,
        borderpad=4,
    )

    # Configure layout with square pixels
    layout = dict(
        margin=dict(l=5, r=5, t=5, b=5, pad=0),
        width=None,
        height=None,
        dragmode="select",
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
        ),
        uirevision="constant",
    )

    # Apply fixed zoom if specified
    if zoom_region:
        x0, x1, y0, y1 = zoom_region
        layout.update(
            xaxis=dict(range=[x0, x1]),
            yaxis=dict(range=[y0, y1], scaleanchor="x", scaleratio=1),
        )

    fig.update_layout(**layout)

    return fig


def create_line_plot(
    selections: List[Tuple[np.ndarray, str, str]],
    tau: Optional[Union[np.ndarray, List]] = None,
    toggle_normalize: Optional[bool] = False,
    current_streamed_g2: Optional[np.ndarray] = None,
    y_zoom_range: Optional[Tuple[float, float]] = None,
):
    """
    Create a line plot for g2 curves.

    Args:
        selections (List[Tuple]): List of (values, name, color) tuples
        toggle_normalize (bool): Whether to normalize values

    Returns:
        plotly.graph_objects.Figure: Plotly figure with line plots
    """

    fig = go.Figure()
    for values, name, color in selections:
        if tau is None:
            tau = list(range(len(values)))
        if toggle_normalize and len(values) > 0:
            # Normalize the values
            values = values / values[0]  # Normalize to the first value
        fig.add_trace(
            go.Scatter(
                x=tau,
                y=values,
                mode="lines",
                name=name,
                line=dict(color=color, width=2),
            )
        )
    if current_streamed_g2 is not None:
        current_streamed_g2 = current_streamed_g2
        if toggle_normalize:
            current_streamed_g2 = current_streamed_g2 / current_streamed_g2[0]
        fig.add_trace(
            go.Scatter(
                x=st.session_state.roi_manager.tau,
                y=current_streamed_g2,
                mode="lines",
                name="Current g2",
                line=dict(color="Grey", width=2, dash="dash"),
            )
        )
    fig.update_layout(
        title="Mean of Selected ROIs",
        xaxis_title="Index or time (log scale)",
        yaxis_title="g2 mean Value",
        width=500,
        height=500,
        xaxis=dict(type="log"),  # Set x-axis to log scale
        yaxis=dict(type="linear"),  # Set y-axis to linear scale
        yaxis_range=y_zoom_range,
    )

    return fig
