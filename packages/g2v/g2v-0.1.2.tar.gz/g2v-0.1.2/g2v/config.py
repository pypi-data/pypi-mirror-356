"""Configuration settings for the g2cubeviewer application."""

import streamlit as st


def show_footer():
    st.markdown(
        """
    ---
    **Use on your own riks. Code can be found on GitHub:** [![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/gnzng/g2v)
    """
    )


# Colors for selections with transparency
COLORS = [
    "rgba(255, 0, 0, 0.8)",  # Red
    "rgba(0, 0, 255, 0.8)",  # Blue
    "rgba(255, 165, 0, 0.8)",  # Orange
    "rgba(128, 0, 128, 0.8)",  # Purple
    "rgba(0, 128, 0, 0.8)",  # Green
    "rgba(255, 192, 203, 0.8)",  # Pink
    "rgba(165, 42, 42, 0.8)",  # Brown
    "rgba(64, 224, 208, 0.8)",  # Turquoise
    "rgba(255, 255, 0, 0.8)",  # Yellow
    "rgba(0, 255, 255, 0.8)",  # Cyan
]

# Get solid colors for the line plot (without transparency)
LINE_COLORS = [color.replace("0.8", "1.0") for color in COLORS]

# Default selection values
DEFAULT_SELECTION = (0, 10, 0, 10)  # (min_row, max_row, min_col, max_col)

# Page layout configuration
PAGE_CONFIG = {"layout": "wide", "page_title": "g2v", "page_icon": "🔎"}
