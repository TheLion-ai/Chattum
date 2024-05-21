import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)


def protect_page():
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["pre-authorized"],
    )
    if st.session_state["authentication_status"] is None:
        authenticator.login()

        st.stop()

    # else:
    #     with st.sidebar:
    #         st.write("Logged in as: ", st.session_state["username"])
    #         authenticator.logout()
