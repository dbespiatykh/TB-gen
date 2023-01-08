import streamlit as st
import base64

from streamlit_extras.mention import mention


def set_page_config():
    try:
        st.set_page_config(
            page_title="TB gen",
            page_icon="./assets/favicon.ico",
            layout="wide",
            initial_sidebar_state="expanded",
        )
    except st.errors.StreamlitAPIException as e:
        if "can only be called once per app" in e.__str__():
            # ignore this error
            return
        raise e


def sidebar_image():

    image_extension = "svg+xml"

    st.markdown(
        f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{image_extension};base64,{base64.b64encode(open('./assets/logo.svg', "rb").read()).decode()});
          padding-top: 80px;
          background-size: 200px;
          background-repeat: no-repeat;
          background-position: 20px 20px;
      }}
      </style>
      """,
        unsafe_allow_html=True,
    )


def github_link():
    with st.sidebar.container():
        st.markdown(
            "This app is maintained by [Dmitry Bespiatykh](https://orcid.org/0000-0003-0867-5988)"
        )
        mention(
            label="dbespiatykh",
            icon="github",
            url="https://github.com/dbespiatykh",
        )
        st.markdown("---")


def set_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
