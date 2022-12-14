import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Phylogeny",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)


def sidebar_bg(side_bg):

    side_bg_ext = "svg+xml"

    st.markdown(
        f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
          padding-top: 100px;
          background-size: 300px;
          background-repeat: no-repeat;
          background-position: 4px 20px;
      }}
      </style>
      """,
        unsafe_allow_html=True,
    )


sidebar_bg("logo.svg")

# TREE TEST
st.header("Lineage 2 Phylogeny")

HtmlTree = open("tree-plot.html", "r", encoding="utf-8")
source_code = HtmlTree.read()
components.html(source_code, height=1500, scrolling=True)


def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1100" height="900" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


show_pdf("l2_tree.pdf")
