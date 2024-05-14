"""Settings page."""

import streamlit as st
from components.sidebar import sidebar_controller
from utils import query_params
from utils.page_config import ensure_bot_or_workflow_selected
import pandas as pd

def read_file(uploaded_file):
    if uploaded_file is not None:
        file_details = uploaded_file.name
        if '.csv' in file_details:
            df = pd.read_csv(uploaded_file)
        elif '.xls' in file_details or '.xlsx' in file_details:
            df = pd.read_excel(uploaded_file)
        else:
            st.error("File type not supported")
            return None
        return df

st.set_page_config(
    page_title="Calibration | Chattum",
    page_icon="⚙️", # TODO change the icon
    # layout="wide"
)

workflow_id = query_params.get_from_url_or_state("workflow_id")
processing_type = query_params.get_from_url_or_state("processing_type")

ensure_bot_or_workflow_selected()
sidebar_controller()


st.title("Upload dataset")

with st.container():
    file_cols = []
    # file_upload_col, _ = st.columns([1, 3])
    # with file_upload_col:
    uploaded_file = st.file_uploader("Choose a file", type=("csv", "xls", "xlsx"))
    df = read_file(uploaded_file)
    if df is not None:
        file_cols = df.columns.tolist()

    source_cols_col, target_cols_col = st.columns([1, 1])
    with source_cols_col:
        option1 = st.selectbox(
            'Select a source column.',
            file_cols
        )
    with target_cols_col:
        option2 = st.selectbox(
            'Select a target column.',
            file_cols
        )
