"""CLI entry point for the Streamlit app. Makes it easy to run the app from the command line as g2v."""
import sys
import os
import streamlit.web.cli as stcli


def main():
    # Get the absolute path to the app.py file
    app_path = os.path.join(os.path.dirname(__file__), "app.py")

    # Set up Streamlit CLI arguments
    sys.argv = ["streamlit", "run", app_path] + sys.argv[1:]

    # Run Streamlit
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
