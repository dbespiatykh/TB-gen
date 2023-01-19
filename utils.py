import streamlit as st
import base64

from streamlit_extras.mention import mention
from streamlit_extras.switch_page_button import switch_page
from st_pages import show_pages_from_config
from st_aggrid import JsCode


@st.experimental_memo(show_spinner=False)
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


@st.experimental_memo(show_spinner=False)
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


@st.experimental_memo(show_spinner=False)
def author_link():
    with st.sidebar.container():
        st.markdown(
            "This app is maintained by  \n[Dmitry Bespiatykh](https://orcid.org/0000-0003-0867-5988)"
        )
        mention(
            label="dbespiatykh",
            icon="github",
            url="https://github.com/dbespiatykh",
        )
        st.markdown("---")


@st.experimental_memo(show_spinner=False)
def set_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


@st.experimental_memo(experimental_allow_widgets=True, show_spinner=False)
def home_page():
    home = st.button("Home")
    if home:
        switch_page("home")


@st.experimental_memo(show_spinner=False)
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
                    if (params.value == 'L1'
                    | params.value == 'L1.1'
                    | params.value == 'L1.1.1'
                    | params.value == 'L1.1.1.1'
                    | params.value == 'L1.1.1.10'
                    | params.value == 'L1.1.1.11'
                    | params.value == 'L1.1.1.2'
                    | params.value == 'L1.1.1.3'
                    | params.value == 'L1.1.1.4'
                    | params.value == 'L1.1.1.5'
                    | params.value == 'L1.1.1.6'
                    | params.value == 'L1.1.1.7'
                    | params.value == 'L1.1.1.8'
                    | params.value == 'L1.1.1.9'
                    | params.value == 'L1.1.2'
                    | params.value == 'L1.1.2.1'
                    | params.value == 'L1.1.2.2'
                    | params.value == 'L1.1.3'
                    | params.value == 'L1.1.3.1'
                    | params.value == 'L1.1.3.2'
                    | params.value == 'L1.1.3.3'
                    | params.value == 'L1.1.3.4'
                    | params.value == 'L1.2'
                    | params.value == 'L1.2'
                    | params.value == 'L1.2.1'
                    | params.value == 'L1.2.2'
                    | params.value == 'L1.2.2.1'
                    | params.value == 'L1.2.2.2'
                    | params.value == 'L1.2.2.3'
                    | params.value == 'L1.2.2.4'
                    | params.value == 'L1.2.2.5'
                    | params.value == 'L1.3'
                    | params.value == 'L1.3'
                    | params.value == 'L1.3.1'
                    | params.value == 'L1.3.2') {
                        return {
                            'color': '#006796',
                            'font-weight': 'bold',
                            'font-family':' sans-serif',
                            'backgroundColor': '#00679633',
                        }
                    }
                    if (params.value == 'L2'
                    | params.value == 'L2.1'
                    | params.value == 'L2.2 (ancient)'
                    | params.value == 'L2.2 (modern)'
                    | params.value == 'L2.2.A'
                    | params.value == 'L2.2.AA1'
                    | params.value == 'L2.2.AA2'
                    | params.value == 'L2.2.AA3'
                    | params.value == 'L2.2.AA3.1'
                    | params.value == 'L2.2.AA3.2'
                    | params.value == 'L2.2.AA4'
                    | params.value == 'L2.2.B'
                    | params.value == 'L2.2.C'
                    | params.value == 'L2.2.D'
                    | params.value == 'L2.2.E'
                    | params.value == 'L2.2.M1'
                    | params.value == 'L2.2.M1.1'
                    | params.value == 'L2.2.M1.2'
                    | params.value == 'L2.2.M1.3'
                    | params.value == 'L2.2.M1.4'
                    | params.value == 'L2.2.M2'
                    | params.value == 'L2.2.M2.1'
                    | params.value == 'L2.2.M2.2'
                    | params.value == 'L2.2.M2.3'
                    | params.value == 'L2.2.M2.4'
                    | params.value == 'L2.2.M2.5'
                    | params.value == 'L2.2.M3'
                    | params.value == 'L2.2.M4'
                    | params.value == 'L2.2.M4.1'
                    | params.value == 'L2.2.M4.2'
                    | params.value == 'L2.2.M4.3'
                    | params.value == 'L2.2.M4.4'
                    | params.value == 'L2.2.M4.5'
                    | params.value == 'L2.2.M4.6'
                    | params.value == 'L2.2.M4.7'
                    | params.value == 'L2.2.M4.8'
                    | params.value == 'L2.2.M4.9'
                    | params.value == 'L2.2.M4.9.1'
                    | params.value == 'L2.2.M4.9.2'
                    | params.value == 'L2.2.M5'
                    | params.value == 'L2.2.M6'
                    | params.value == 'L2.2.M6.1'
                    | params.value == 'L2.2.M6.2'
                    | params.value == '2.2.1.2'
                    | params.value == 'AA1SA'
                    | params.value == 'Bmyc3'
                    | params.value == 'lin2.2.1.2') {
                        return {
                            'color': '#8A517E',
                            'font-weight': 'bold',
                            'font-family':' sans-serif',
                            'backgroundColor': '#8A517E33',
                        }
                    }
                    if (params.value == 'L3'
                    | params.value == 'L3.1'
                    | params.value == 'L3.1.1'
                    | params.value == 'L3.1.1.1'
                    | params.value == 'L3.1.1.2'
                    | params.value == 'L3.1.2'
                    | params.value == 'L3.1.3'
                    | params.value == 'L3.1.3.1'
                    | params.value == 'L3.2'
                    | params.value == 'L3.2'
                    | params.value == 'L3.3'
                    | params.value == 'L3.3'
                    | params.value == 'L3.4'
                    | params.value == 'L3.4'
                    | params.value == 'L3.5'
                    | params.value == 'L3.5'
                    | params.value == 'L3.5.1'
                    | params.value == 'L3.6'
                    | params.value == 'L3.6') {
                        return {
                            'color': '#B56748',
                            'font-weight': 'bold',
                            'font-family':' sans-serif',
                            'backgroundColor': '#B5674833',
                        }
                    }
                    if (params.value == 'L4'
                    | params.value == 'L4.1'
                    | params.value == 'L4.1.1'
                    | params.value == 'L4.1.1.1'
                    | params.value == 'L4.1.1.2'
                    | params.value == 'L4.1.1.3'
                    | params.value == 'L4.1.1.3.1'
                    | params.value == 'L4.1.2'
                    | params.value == 'L4.1.2.1'
                    | params.value == 'L4.1.2.1.1'
                    | params.value == 'L4.1.3'
                    | params.value == 'L4.1.4'
                    | params.value == 'L4.2'
                    | params.value == 'L4.2'
                    | params.value == 'L4.2.1'
                    | params.value == 'L4.2.1.1'
                    | params.value == 'L4.2.2'
                    | params.value == 'L4.2.2.1'
                    | params.value == 'L4.2.2.2'
                    | params.value == 'L4.3'
                    | params.value == 'L4.3'
                    | params.value == 'L4.3.1'
                    | params.value == 'L4.3.1.1'
                    | params.value == 'L4.3.2'
                    | params.value == 'L4.3.2.1'
                    | params.value == 'L4.3.3'
                    | params.value == 'L4.3.4'
                    | params.value == 'L4.3.4.1'
                    | params.value == 'L4.3.4.2'
                    | params.value == 'L4.3.4.2.1'
                    | params.value == 'L4.4'
                    | params.value == 'L4.4'
                    | params.value == 'L4.4.1'
                    | params.value == 'L4.4.1.1'
                    | params.value == 'L4.4.1.1.1'
                    | params.value == 'L4.4.1.2'
                    | params.value == 'L4.4.2'
                    | params.value == 'L4.5'
                    | params.value == 'L4.5'
                    | params.value == 'L4.6'
                    | params.value == 'L4.6'
                    | params.value == 'L4.6.1'
                    | params.value == 'L4.6.1.1'
                    | params.value == 'L4.6.1.2'
                    | params.value == 'L4.6.2'
                    | params.value == 'L4.6.2.2'
                    | params.value == 'L4.6.3'
                    | params.value == 'L4.6.4'
                    | params.value == 'L4.6.5'
                    | params.value == 'L4.7'
                    | params.value == 'L4.7'
                    | params.value == 'L4.8'
                    | params.value == 'L4.8'
                    | params.value == 'L4.8.1'
                    | params.value == 'L4.8.2'
                    | params.value == 'L4.8.3'
                    | params.value == 'L4.9'
                    | params.value == 'L4.9'
                    | params.value == 'L4.9.1') {
                        return {
                            'color': '#16592C',
                            'font-weight': 'bold',
                            'font-family':' sans-serif',
                            'backgroundColor': '#16592C33',
                        }
                    }
                    if (params.value == 'L5'
                    | params.value == 'L5.1'
                    | params.value == 'L5.1.1'
                    | params.value == 'L5.1.2'
                    | params.value == 'L5.1.3'
                    | params.value == 'L5.1.4'
                    | params.value == 'L5.1.5'
                    | params.value == 'L5.2'
                    | params.value == 'L5.2'
                    | params.value == 'L5.3'
                    | params.value == 'L5.3') {
                        return {
                            'color': '#595480',
                            'font-weight': 'bold',
                            'font-family':' sans-serif',
                            'backgroundColor': '#59548033',
                        }
                    }
                    if (params.value == 'L6'
                    | params.value == 'L6.1'
                    | params.value == 'L6.1.1'
                    | params.value == 'L6.1.2'
                    | params.value == 'L6.1.3'
                    | params.value == 'L6.2'
                    | params.value == 'L6.2'
                    | params.value == 'L6.2.1'
                    | params.value == 'L6.2.2'
                    | params.value == 'L6.2.3'
                    | params.value == 'L6.3'
                    | params.value == 'L6.3'
                    | params.value == 'L6.3.1'
                    | params.value == 'L6.3.2'
                    | params.value == 'L6.3.3') {
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
                    if (params.value == 'M.bovis'
                    | params.value == 'M.caprae'
                    | params.value == 'M.microti'
                    | params.value == 'M.orygis'
                    | params.value == 'M.pinipedii') {
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
