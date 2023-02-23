import json
import base64
import string
import random
import streamlit as st
import streamlit.components.v1 as components

from st_aggrid import JsCode
from st_pages import show_pages_from_config
from streamlit_extras.switch_page_button import switch_page
from streamlit_lottie import st_lottie, st_lottie_spinner


def get_random_key(size=6, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


@st.cache_data(show_spinner=False)
def set_pages():
    show_pages_from_config()


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


@st.cache_data(show_spinner=False)
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


@st.cache_data(show_spinner=False)
def author_link():
    with st.sidebar.container():
        st.markdown(
            """
            <a href="https://www.researchgate.net/profile/Dmitry-Bespiatykh"><img
                src="https://img.shields.io/badge/Dmitry_Bespiatykh-00CCBB?logo=researchgate&amp;style=flat-square&amp;labelColor=white&amp;logoWidth=20&amp;logoColor=00CCBB"
                alt="RG"
            /></a>
            <a href="https://orcid.org/0000-0003-0867-5988"><img
                src="https://img.shields.io/badge/0000_0003_0867_5988-A6CE39?logo=orcid&amp;style=flat-square&amp;labelColor=white&amp;logoWidth=20"
                alt="ORCiD"
            /></a>
            <a href="https://github.com/dbespiatykh"><img
                src="https://img.shields.io/badge/dbespiatykh-181717?logo=github&amp;style=flat-square&amp;labelColor=white&amp;logoWidth=20&amp;logoColor=181717"
                alt="GitHub"
            /></a>
            """,
            unsafe_allow_html=True,
        )


@st.cache_data(show_spinner=False)
def set_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


@st.cache_data(experimental_allow_widgets=True, show_spinner=False)
def home_page():
    home = st.button("Home")
    if home:
        switch_page("home")


@st.cache_data(experimental_allow_widgets=True, show_spinner=False)
def read_index_html():
    with open("index.html") as f:
        components.html(
            f.read(),
            height=0,
            width=0,
        )


def lottie_success():
    with open("./assets/lottiefiles/success.json") as f:
        animation = json.load(f)
        return st_lottie(animation, loop=False, key="success", height=150)


def lottie_error():
    with open("./assets/lottiefiles/error.json") as f:
        animation = json.load(f)
        return st_lottie(animation, loop=True, key="error", height=100)


def lottie_warning():
    with open("./assets/lottiefiles/warning.json") as f:
        animation = json.load(f)
        return st_lottie(animation, loop=True, key="warning", height=100)


def lottie_arrow():
    with open("./assets/lottiefiles/arrow.json") as f:
        animation = json.load(f)
        return st_lottie(animation, loop=False, key="initial", height=100, speed=1.5)


def lottie_spinner():
    with open("./assets/lottiefiles/spinner.json") as f:
        animation = json.load(f)
        return st_lottie_spinner(animation, loop=True, height=100, key=get_random_key())


def back_button(anchor: str):
    link = f"#{anchor}"
    st.markdown(
        f"""
        <a
        style="text-decoration: none"
        href="{link}">
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            fill="#7A3777"
            class="bi bi-arrow-up-square-fill"
            viewBox="0 0 16 16">
            <path
            d="M2 16a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2zm6.5-4.5V5.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 5.707V11.5a.5.5 0 0 0 1 0z"/>
        </svg>
        <span style="color: #a65aa3; font-weight: bold">Back to top</span>
        </a>
            """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def get_cell_style():
    cellstyle_jscode = JsCode(
        """
                function(params){
                    if (params.value == 'A') {
                        return {
                            'color': '#C22005',
                            'font-weight': 'bold',
                            'font-family': 'sans-serif',
                        }
                    }
                    if (params.value == 'T') {
                        return{
                            'color': '#00BC0C',
                            'font-weight': 'bold',
                            'font-family': 'sans-serif',
                        }
                    }
                    if (params.value == 'G') {
                        return{
                            'color': '#BBAE0C',
                            'font-weight': 'bold',
                            'font-family': 'sans-serif',
                        }
                    }
                    if (params.value == 'C') {
                        return{
                            'color': '#0529C0',
                            'font-weight': 'bold',
                            'font-family': 'sans-serif',
                        }
                    }
                    var re = new RegExp("^L1");
                    if (re.test(params.value)){
                        return {
                            'color': '#006796',
                            'font-weight': 'bold',
                            'font-family':' sans-serif',
                            'backgroundColor': '#00679633',
                        }
                    }
                    var re = new RegExp("^L2|^Bmyc|^AA1|^lin2|2.2.1.2");
                    if (re.test(params.value)){
                        return {
                            'color': '#8A517E',
                            'font-weight': 'bold',
                            'font-family':' sans-serif',
                            'backgroundColor': '#8A517E33',
                        }
                    }
                    var re = new RegExp("^L3");
                    if (re.test(params.value)){
                        return {
                            'color': '#B56748',
                            'font-weight': 'bold',
                            'font-family':' sans-serif',
                            'backgroundColor': '#B5674833',
                        }
                    }
                    var re = new RegExp("^L4");
                    if (re.test(params.value)){
                        return {
                            'color': '#16592C',
                            'font-weight': 'bold',
                            'font-family':' sans-serif',
                            'backgroundColor': '#16592C33',
                        }
                    }
                    var re = new RegExp("^L5");
                    if (re.test(params.value)){
                        return {
                            'color': '#595480',
                            'font-weight': 'bold',
                            'font-family':' sans-serif',
                            'backgroundColor': '#59548033',
                        }
                    }
                    var re = new RegExp("^L6");
                    if (re.test(params.value)){
                        return {
                            'color': '#696969',
                            'font-weight': 'bold',
                            'font-family':' sans-serif',
                            'backgroundColor': '#69696933',
                        }
                    }
                    if (params.value == 'L7') {
                        return {
                            'color': '#69523D',
                            'font-weight': 'bold',
                            'font-family':' sans-serif',
                            'backgroundColor': '#69523D33',
                        }
                    }
                    if (params.value == 'L8') {
                        return {
                            'color': '#406094',
                            'font-weight': 'bold',
                            'font-family':' sans-serif',
                            'backgroundColor': '#40609433',
                        }
                    }
                    if (params.value == 'L9') {
                        return {
                            'color': '#3B8087',
                            'font-weight': 'bold',
                            'font-family':' sans-serif',
                            'backgroundColor': '#3B808733',
                        }
                    }
                    var re = new RegExp("^M.");
                    if (re.test(params.value)){
                        return {
                            'color': '#82181A',
                            'font-weight': 'bold',
                            'font-family':' sans-serif',
                            'backgroundColor': '#82181A33',
                        }
                    }
                }
                """
    )
    return cellstyle_jscode
