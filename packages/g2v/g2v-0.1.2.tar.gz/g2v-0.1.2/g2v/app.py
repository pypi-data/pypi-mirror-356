import streamlit as st
import numpy as np
import pandas as pd

from config import COLORS, LINE_COLORS, PAGE_CONFIG, show_footer
from roi_manager import ROIManager
from plotting import create_heatmap_with_selections, create_line_plot
from utils import save_data_to_h5, prepare_g2_data_for_export
from data_processing import h5_file_checks, get_mean_g2_for_roi
import h5py


# Initialize session state
def initialize_session_state():
    """Initialize session state variables."""
    if "roi_manager" not in st.session_state:
        # Initialize ROIManager with default image dimensions
        st.session_state.roi_manager = ROIManager(1024, 1024)
    if "current_streamed_g2" not in st.session_state:
        st.session_state.current_streamed_g2 = None
    if "image" not in st.session_state:
        st.session_state.image = np.array([[1, 0], [0, 1]])


# Update current ROI selection based on input values
def update_current_selection():
    """Update the current selection in the ROI manager."""
    roi_manager = st.session_state.roi_manager
    roi_manager.update_current_selection(
        st.session_state.min_row,
        st.session_state.max_row,
        st.session_state.min_col,
        st.session_state.max_col,
    )


# Render the image panel (left column)
def render_image_panel():
    """Render the image panel with heatmap and selection controls."""
    roi_manager = st.session_state.roi_manager

    # Color scaling controls
    col1, col2, col3 = st.columns(3)
    with col1:
        color_scale_min = st.slider(
            "Color Scale Min",
            min_value=float(np.min(st.session_state.image)),
            max_value=float(np.max(st.session_state.image)),
            value=float(np.min(st.session_state.image)),
            step=0.1,
        )
    with col2:
        color_scale_max = st.slider(
            "Color Scale Max",
            min_value=float(np.min(st.session_state.image)),
            max_value=float(np.max(st.session_state.image)),
            value=float(np.max(st.session_state.image)),
            step=0.1,
        )
    with col3:
        colormap = st.selectbox(
            "Colormap",
            options=[
                "Greys",
                "Viridis",
                "Plasma",
                "Inferno",
                "Magma",
                "Cividis",
                "Blues",
                "Reds",
                "Hot",
                "Jet",
                "Rainbow",
            ],
            index=0,
        )

    # Zoom controls
    zoom_col, zoom_col2 = st.columns(2)
    with zoom_col:
        zoom_enabled = st.checkbox("Lock zoom", value=False)
    with zoom_col2:
        factor = st.selectbox(
            "Factor for rebinning", options=[1, 2, 4, 8, 16, 32], index=5
        )
    zoom_region = None
    if zoom_enabled:
        st.write("Zoom region:")
        z1, z2, z3, z4 = st.columns(4, gap="small")
        with z1:
            zoom_x0 = st.number_input("X min", value=0, step=100)
        with z2:
            zoom_x1 = st.number_input("X max", value=100, step=100)
        with z3:
            zoom_y0 = st.number_input("Y min", value=0, step=100)
        with z4:
            zoom_y1 = st.number_input("Y max", value=100, step=100)
        zoom_region = (zoom_x0, zoom_x1, zoom_y0, zoom_y1)

    # Display heatmap
    st.plotly_chart(
        create_heatmap_with_selections(
            st.session_state.image,
            roi_manager.selection_rects,
            roi_manager.selection_colors,
            roi_manager.current_selection,
            color_scale_min,
            color_scale_max,
            zoom_region if zoom_enabled else None,
            colormap,
            factor,
        ),
        use_container_width=True,
        config={"scrollZoom": True},
    )


# Render the selection panel (middle column)
def render_selection_panel():
    """Render the selection panel with ROI selection controls with buttons."""
    roi_manager = st.session_state.roi_manager

    st.write("### Selection Parameters")

    # Selection inputs
    left_col, right_col = st.columns(2)
    with left_col:
        st.number_input(
            "Min Row",
            value=roi_manager.current_selection[0],
            key="min_row",
            on_change=update_current_selection,
            step=100,
        )
        st.number_input(
            "Max Row",
            value=roi_manager.current_selection[1],
            key="max_row",
            on_change=update_current_selection,
            step=100,
        )
    with right_col:
        st.number_input(
            "Min Column",
            value=roi_manager.current_selection[2],
            key="min_col",
            on_change=update_current_selection,
            step=100,
        )
        st.number_input(
            "Max Column",
            value=roi_manager.current_selection[3],
            key="max_col",
            on_change=update_current_selection,
            step=100,
        )

    # Selection info
    min_row, max_row = (
        roi_manager.current_selection[0],
        roi_manager.current_selection[1],
    )
    min_col, max_col = (
        roi_manager.current_selection[2],
        roi_manager.current_selection[3],
    )
    st.session_state.current_streamed_g2 = get_mean_g2_for_roi(
        st.session_state.roi_manager.g2cube,
        roi_manager.selected_indices,
    )

    st.write(f"**Current selection:** ({min_row}, {max_row}, {min_col}, {max_col})")
    st.write(f"**Number of pixels:** {len(roi_manager.selected_indices)}")

    # Action buttons
    st.write("### Actions")
    if st.button("Add Current Selection to Plot", icon="➕"):
        if roi_manager.selected_indices:
            color_idx = len(roi_manager.selections) % len(COLORS)
            line_color = LINE_COLORS[color_idx]
            selection_name = f"Selection {len(roi_manager.selections) + 1}"
            mean_g2_for_roi = st.session_state.current_streamed_g2
            roi_manager.add_selection(mean_g2_for_roi, selection_name, line_color)
            st.success(f"Added {selection_name}")
        else:
            st.error("No selection processed")

    if st.button("Clear All Selections", icon="🗑️"):
        roi_manager.clear_selections()
        st.success("Cleared all selections")


# Render the plot panel (right column)
def render_plot_panel():
    """Render the plot panel with line chart and download options for different files."""
    roi_manager = st.session_state.roi_manager

    colline1, colline2 = st.columns(2)
    with colline1:
        toggle_normalize = st.checkbox("Normalize to g2[tau=first point]", value=True)
    with colline2:
        y_zoom_enabled = st.checkbox("Enable Y-Axis Zoom", value=False)
    y_zoom_range = None
    if y_zoom_enabled:
        colzoom1, colzoom2 = st.columns(2)
        with colzoom1:
            y_min = st.number_input("Y-Axis Min", value=0.0, step=0.1, format="%.6f")
        with colzoom2:
            y_max = st.number_input("Y-Axis Max", value=1.0, step=0.001, format="%.6f")
        y_zoom_range = (y_min, y_max)

    # Plot the line chart
    st.plotly_chart(
        create_line_plot(
            roi_manager.selections,
            tau=roi_manager.tau,
            toggle_normalize=toggle_normalize,
            current_streamed_g2=st.session_state.current_streamed_g2,
            y_zoom_range=y_zoom_range,
        ),
        use_container_width=True,
    )

    # Download data section
    if len(roi_manager.selections) > 0:
        tau = roi_manager.tau
        roi_df = roi_manager.get_selection_dataframe()
        g2_data = prepare_g2_data_for_export(roi_manager.selections)

        st.download_button(
            label="Download ROI and g2 Data as h5",
            data=save_data_to_h5(
                roi_df, g2_data, tau, st.session_state.image
            ).getvalue(),
            file_name="roi_and_g2_data.h5",
            mime="application/octet-stream",
            icon="💾",
        )

    # Display data for copying
    st.write("Use the code block to easily copy the g2 data to clipboard:")
    # Show data for selections or streamed g2
    if roi_manager.selections:
        tau = roi_manager.tau
        g2_data = {"Tau": np.around(tau, 3)}

        if toggle_normalize:
            g2_data.update(
                {name: values / values[0] for values, name, _ in roi_manager.selections}
            )
        else:
            g2_data.update({name: values for values, name, _ in roi_manager.selections})

        g2_csv = pd.DataFrame(g2_data).to_csv(index=False, sep="\t")
        st.code(g2_csv, height=200, language="text")
    else:
        st.warning("No ROI selections available to copy.")


# Render file upload mode UI
def render_file_upload_mode():
    """Render the file upload mode UI and save the data to session state."""
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Upload a file (optional)", type=["h5"])
        if uploaded_file is not None:
            h5_file_checks(uploaded_file)
            with h5py.File(uploaded_file, "r") as h5_file:
                if "Detector_Image" in h5_file:
                    st.session_state.image = h5_file["Detector_Image"][:]
                    (
                        st.session_state.roi_manager.image_height,
                        st.session_state.roi_manager.image_width,
                    ) = (
                        st.session_state.image.shape[0],
                        st.session_state.image.shape[1],
                    )
                    st.session_state.roi_manager.tau = h5_file["tau_log"][:]
                    st.session_state.roi_manager.g2cube = h5_file["g2_Curves"][:]
                    st.write("File uploaded successfully.")
                else:
                    st.error(
                        "The uploaded file does not contain a 'Detector_Image' dataset."
                    )


# Main application function
def main():
    """Main function to run the Streamlit app."""
    # Configure the page
    st.set_page_config(**PAGE_CONFIG)

    # App title and description
    st.title("🔍📦 g2v")
    st.write(
        "This is a simple viewer for g2cube data. You can select regions of interest and "
        "visualize the mean values."
    )

    render_file_upload_mode()
    initialize_session_state()

    # Create the three-column layout
    col1, col2, col3 = st.columns([4, 3, 4])

    with col1:
        render_image_panel()

    with col2:
        render_selection_panel()

    with col3:
        render_plot_panel()

    # Footer
    show_footer()


if __name__ == "__main__":
    main()
