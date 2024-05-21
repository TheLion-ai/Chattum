"""Settings page."""

import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
from backend_controller import evaluate_workflow, get_workflow
from components.authentication import protect_page
from components.sidebar import sidebar_controller
from components.workflows import ClassificationEvaluation
from streamlit.runtime.uploaded_file_manager import UploadedFile
from streamlit_extras.metric_cards import style_metric_cards
from utils import query_params
from utils.page_config import ensure_bot_or_workflow_selected

st.set_page_config(
    page_title="Evaluation | Chattum",
    page_icon="⚖",
)


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


workflow_id = query_params.get_from_url_or_state("workflow_id")
processing_type = query_params.get_from_url_or_state("processing_type")

ensure_bot_or_workflow_selected()
sidebar_controller()
protect_page()


workflow = get_workflow(workflow_id)
if workflow["task"].lower() != "classification":
    st.error("Evaluation is only supported for classification workflows.")
    st.stop()

style_metric_cards()

with st.container():
    with st.expander("Upload dataset", expanded=True):
        st.write(
            "Upload a dataset to evaluate the performance of the model. The dataset should contain the source and target columns."
        )
        file_cols = []
        # file_upload_col, _ = st.columns([1, 3])
        # with file_upload_col:
        uploaded_file = st.file_uploader("Choose a file", type=("csv", "xls", "xlsx"))
        df = read_file(uploaded_file)  # type: ignore
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
            calibrate_button = st.button("Evaluate", use_container_width=True)
        if calibrate_button:
            x = df[option1].tolist()[:100]
            y = df[option2].tolist()[:100]
            with st.spinner("Evaluating..."):
                metrics = evaluate_workflow(workflow_id, x, y)
                ClassificationEvaluation(workflow, metrics)()
