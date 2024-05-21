"""Page for chatting with the bot."""

from datetime import datetime, timedelta

import pandas as pd
import pytz
import streamlit as st
from backend_controller import get_conversations
from components.conversations import display_conversation
from components.sidebar import sidebar_controller
from streamlit_chat import message
from streamlit_date_picker import PickerType, Unit, date_picker, date_range_picker
from utils import query_params
from utils.page_config import ensure_bot_or_workflow_selected
from components.authentication import protect_page

st.set_page_config(
    page_title="Conversations | Chattum",
    page_icon="💬",
    layout="wide",
)

bot_id = query_params.get_from_url_or_state("bot_id")
conversation_id = query_params.get_from_url_or_state("conversation_id")
timezone = pytz.timezone("Europe/Warsaw")

ensure_bot_or_workflow_selected()
sidebar_controller()
protect_page()


conversations = get_conversations(bot_id)

current_conversation = next(
    (x for x in conversations if x["id"] == conversation_id), None
)
st.title("Conversations")

col1, col2, col3, col4 = st.columns([4, 4, 4, 4])
with col1:
    start_date = st.date_input(
        "Start Date",
        key="start_date",
        value=datetime.now() - timedelta(days=1),
    )
with col2:
    start_time = st.time_input(
        "Start Time", key="start_time", value=datetime.now(tz=timezone).time()
    )
with col3:
    end_date = st.date_input("End Date", key="end_date", value=datetime.now())
with col4:
    end_time = st.time_input(
        "End Time", key="end_time", value=datetime.now(tz=timezone).time()
    )

# filter conversations by date
start_datetime = datetime.combine(start_date, start_time)
end_datetime = datetime.combine(end_date, end_time)
filtered_conversations = []
for conversation in conversations:
    conversation_date = datetime.strptime(
        conversation["last_message_time"], "%Y-%m-%dT%H:%M:%S.%f"
    )
    if start_datetime <= conversation_date <= end_datetime:
        filtered_conversations.append(conversation)
conversations = filtered_conversations

stats_container = st.expander("Statistics")
st.write("")
conversation_list, conversation_content = st.columns([3, 5], gap="large")
with conversation_list:
    conversation_list_container = st.container()
with conversation_content:
    conversation_content_container = st.container()

if conversations == []:
    st.write("No conversations yet!")
else:
    with stats_container:
        col1, col2 = st.columns([3, 1])
        with col1:
            # Generate a line chart showing the number of conversations in each hour for the time range

            # Create a DataFrame to hold conversation counts per hour
            conversation_counts = pd.DataFrame(columns=["Hour", "Count"])

            # Initialize the start hour
            current_hour = start_datetime.replace(minute=0, second=0, microsecond=0)

            # Count conversations for each hour in the range
            while current_hour <= end_datetime:
                # Find conversations in the current hour
                hour_end = current_hour + timedelta(hours=1)
                count = sum(
                    1
                    for conversation in conversations
                    if current_hour
                    <= datetime.strptime(
                        conversation["last_message_time"], "%Y-%m-%dT%H:%M:%S.%f"
                    )
                    < hour_end
                )
                # Append the count to the DataFrame
                conversation_counts = pd.concat(
                    [
                        conversation_counts,
                        pd.DataFrame(
                            [
                                {
                                    "Hour": current_hour.strftime("%d %b %Y %H:%M"),
                                    "Count": count,
                                }
                            ]
                        ),
                    ],
                    ignore_index=True,
                )
                # Move to the next hour
                current_hour = hour_end

            # Plot the line chart
            import altair as alt

            # Create a line chart using Altair
            line_chart = (
                alt.Chart(conversation_counts)
                .mark_bar()
                .encode(
                    x="Hour:T",
                    y="Count:Q",
                    color=alt.value("#2993fa"),  # Set the color of the line
                    tooltip=["Hour:T", "Count:Q"],
                )
                .properties(
                    width=700,  # Optional: you can set the width of the chart
                    height=400,  # Optional: you can set the height of the chart
                    title=alt.TitleParams(text="Conversations", anchor="middle"),
                )
            )

            # Display the chart in Streamlit
            st.altair_chart(line_chart, use_container_width=True)
        with col2:
            # Count tool usage in conversations
            tool_usage: dict = {}
            for conversation in conversations:
                for bot_message in conversation["messages"]:
                    if "tool_calls" in bot_message["data"]:
                        for tool_call in bot_message["data"]["tool_calls"]:
                            tool_name = tool_call["name"]
                            tool_usage[tool_name] = tool_usage.get(tool_name, 0) + 1

            # Create a DataFrame for the tool usage
            tool_usage_df = pd.DataFrame(
                list(tool_usage.items()), columns=["Tool", "Usage"]
            )

            # Plot the pie chart
            pie_chart = (
                alt.Chart(tool_usage_df)
                .mark_arc()
                .encode(
                    theta=alt.Theta(field="Usage", type="quantitative"),
                    color=alt.Color(
                        field="Tool",
                        type="nominal",
                        legend=None,
                    ),
                    tooltip=["Tool", "Usage"],
                )
                .properties(
                    title=alt.TitleParams(text="Tool Usage", anchor="middle"),
                    # width=400,  # Adjust the width as needed
                    # height=300,  # Adjust the height as needed
                )
            )

            # Display the pie chart with a legend in Streamlit
            st.altair_chart(pie_chart, use_container_width=True)
    with conversation_list_container:
        # Sort conversations by timestamp
        conversations = sorted(
            conversations,
            key=lambda x: (
                x.get("last_message_time")
                if x.get("last_message_time") is not None
                else ""
            ),
            reverse=True,
        )

        for conversation in conversations:
            # Reformat the date
            format_1 = "%Y-%m-%dT%H:%M:%S.%f"
            format_2 = "%d/%m/%Y %H:%M:%S"
            last_message_time_str = (
                datetime.strptime(conversation["last_message_time"], format_1).strftime(
                    format_2
                )
                if conversation.get("last_message_time") is not None
                else ""
            )

            st.button(
                last_message_time_str,
                use_container_width=True,
                on_click=query_params.set_to_url,
                kwargs={"conversation_id": conversation["id"]},
                type=(
                    "primary" if conversation_id == conversation["id"] else "secondary"
                ),
                key=conversation["id"],
            )

with conversation_content_container:
    if current_conversation:
        display_conversation(current_conversation)
        with st.expander("Debug"):
            st.write(current_conversation)
