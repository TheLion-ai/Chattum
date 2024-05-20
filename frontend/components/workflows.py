import pandas as pd
import plotly.express as px
import streamlit as st
from backend_controller import create_or_edit_workflow


class ClassificationEvaluation:
    def __init__(self, workflow: dict, metrics: dict) -> None:
        self.workflow = workflow
        self.metrics = metrics

    def __class_metric(self, class_name: str, editable_thresholds: bool) -> None:
        with st.expander(f"Class: {class_name}", expanded=False):
            st.dataframe(
                pd.DataFrame(
                    {
                        "Precision": [round(self.metrics[class_name]["precision"], 3)],
                        "Recall": [round(self.metrics[class_name]["recall"], 3)],
                        "F1": [round(self.metrics[class_name]["f1-score"], 3)],
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
            st.markdown("#### ROC Curve")
            st.line_chart(
                pd.DataFrame(
                    {
                        "True Positive Rate": self.metrics[class_name]["tpr"],
                        "False Positive Rate": self.metrics[class_name]["fpr"],
                    }
                ),
                x="False Positive Rate",
                y="True Positive Rate",
            )
            st.markdown("#### Precision-Recall Curve")
            fig = px.line(
                pd.DataFrame(
                    {
                        "Precision": self.metrics[class_name]["precisions"],
                        "Recall": self.metrics[class_name]["recalls"],
                        "Threshold": self.metrics[class_name]["p_r_thresholds"] + [1],
                    }
                ),
                x="Recall",
                y="Precision",
                hover_data="Threshold",
            )
            st.plotly_chart(fig, use_container_width=True)
            if editable_thresholds:
                st.markdown("##### Threshold")

                col1, col2 = st.columns([3, 1])
                with col1:
                    self.workflow["class_thresholds"][class_name] = st.number_input(
                        "Threshold",
                        0.0,
                        1.0,
                        self.workflow["class_thresholds"][class_name],
                        key=f"{class_name}_threshold",
                        label_visibility="collapsed",
                    )
                with col2:
                    if st.button(
                        "Save", key=f"{class_name}_save", use_container_width=True
                    ):
                        create_or_edit_workflow(self.workflow)

    def __average_metric(self) -> None:
        with st.expander("Average Metrics", expanded=True):

            col1, _, col2 = st.columns(3)

            col1.dataframe(
                pd.DataFrame({"Accuracy": [round(self.metrics["accuracy"], 3)]}),
                use_container_width=True,
                hide_index=True,
            )
            st.markdown("#### Macro Average")

            st.dataframe(
                pd.DataFrame(
                    {
                        "Precision": [round(self.metrics["macro avg"]["precision"], 3)],
                        "Recall": [round(self.metrics["macro avg"]["recall"], 3)],
                        "F1": [round(self.metrics["macro avg"]["f1-score"], 3)],
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
            st.markdown("#### Weighted Average")
            st.dataframe(
                pd.DataFrame(
                    {
                        "Precision": [
                            round(self.metrics["weighted avg"]["precision"], 3)
                        ],
                        "Recall": [round(self.metrics["weighted avg"]["recall"], 3)],
                        "F1": [round(self.metrics["weighted avg"]["f1-score"], 3)],
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

    def __call__(self, editable_thresholds: bool = False) -> None:
        st.title("Evaluation Results")
        # with st.expander("Debug", expanded=False):
        # st.write(self.metrics)
        st.write("### Average Metrics")
        self.__average_metric()
        st.write("### Class Metrics")
        for class_name in self.workflow["classes"]:
            self.__class_metric(class_name, editable_thresholds)
