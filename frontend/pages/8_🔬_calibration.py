"""Settings page."""

from copy import deepcopy

import pandas as pd
import streamlit as st
from backend_controller import calibrate_workflow_model, evaluate_workflow, get_workflow
from components.sidebar import sidebar_controller
from components.workflows import ClassificationEvaluation
from streamlit.runtime.uploaded_file_manager import UploadedFile
from utils import query_params
from utils.page_config import ensure_bot_or_workflow_selected
from components.authentication import protect_page


def read_file(uploaded_file: UploadedFile) -> pd.DataFrame:
    if uploaded_file is not None:
        file_details = uploaded_file.name
        if ".csv" in file_details:
            df = pd.read_csv(uploaded_file)
        elif ".xls" in file_details or ".xlsx" in file_details:
            df = pd.read_excel(uploaded_file)
        else:
            st.error("File type not supported")
            return None
        return df


st.set_page_config(
    page_title="Calibration | Chattum",
    page_icon="⚙️",  # TODO change the icon
    # layout="wide"
)

workflow_id = query_params.get_from_url_or_state("workflow_id")
processing_type = query_params.get_from_url_or_state("processing_type")

ensure_bot_or_workflow_selected()
sidebar_controller()
protect_page()

workflow = get_workflow(workflow_id)
if workflow["task"].lower() != "classification":
    st.error("Calibration is only supported for classification workflows.")
    st.stop()

st.title("Upload dataset")

with st.container():
    with st.expander("Upload dataset", expanded=True):
        st.write(
            "Upload a dataset to evaluate the performance of the model. The dataset should contain the source and target columns."
        )
        file_cols = []
        # file_upload_col, _ = st.columns([1, 3])
        # with file_upload_col:
        uploaded_file = st.file_uploader("Choose a file", type=("csv", "xls", "xlsx"))
        df = read_file(uploaded_file)
        st.write(df.head() if df is not None else None)
        if df is not None:
            file_cols = df.columns.tolist()

        source_cols_col, target_cols_col = st.columns([1, 1])
        with source_cols_col:
            option1 = st.selectbox("Select a source column.", file_cols)
        with target_cols_col:
            option2 = st.selectbox("Select a target column.", file_cols)
    if option1 and option2:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col3:
            calibrate_button = st.button("Calibrate", use_container_width=True)
        if calibrate_button:
            x = df[option1].tolist()[:100]
            y = df[option2].tolist()[:100]
            with st.spinner("Calibrating..."):
                calibrate_workflow_model(workflow_id, x, y)
            st.toast("Callibration finished, running evaluation", icon="ℹ️")
            with st.spinner("Evaluating..."):
                st.session_state["metrics"] = evaluate_workflow(workflow_id, x, y)
    if "metrics" in st.session_state:
        st.info(
            "Calibration and evaluation finished. Now you inspect the results can adjust the threshold for each class.",
            icon="ℹ️",
        )
        ClassificationEvaluation(deepcopy(workflow), st.session_state["metrics"])(
            editable_thresholds=True
        )
