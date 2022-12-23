import base64
import streamlit as st

from utils import set_page_config, sidebar_image, set_css
import streamlit.components.v1 as components


set_page_config()
sidebar_image()
set_css()

st.title("_Mycobacterium tuberculosis_ phylogeny")

st.markdown("---")


def show_lineage1_tree():
    HtmlTree = open("./data/trees/lineage.1.tree.html", "r", encoding="utf-8")
    source_code = HtmlTree.read()
    components.html(source_code, height=1000, width=1800, scrolling=True)


def show_lineage2_tree():
    HtmlTree = open("./data/trees/lineage.2.tree.html", "r", encoding="utf-8")
    source_code = HtmlTree.read()
    components.html(source_code, height=1000, width=1800, scrolling=True)


def show_lineage3_tree():
    HtmlTree = open("./data/trees/lineage.3.tree.html", "r", encoding="utf-8")
    source_code = HtmlTree.read()
    components.html(source_code, height=1000, width=1800, scrolling=True)


def show_lineage4_tree():
    HtmlTree = open("./data/trees/lineage.4.tree.html", "r", encoding="utf-8")
    source_code = HtmlTree.read()
    components.html(source_code, height=1000, width=1800, scrolling=True)


def show_lineage5_tree():
    HtmlTree = open("./data/trees/lineage.5.Animal.tree.html", "r", encoding="utf-8")
    source_code = HtmlTree.read()
    components.html(source_code, height=1000, width=1600, scrolling=True)


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Lineage 1",
        "Lineage 2",
        "Lineage 3",
        "Lineage 4",
        "Lineage 5-Animal",
    ]
)

with tab1:
    show_lineage1_tree()

with tab2:
    show_lineage2_tree()

with tab3:
    show_lineage3_tree()

with tab4:
    show_lineage4_tree()

with tab5:
    show_lineage5_tree()


# def show_svg(file_path):
#     with open(file_path, "rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode("utf-8")
#     pdf_display = f'<iframe src="data:image/svg+xml;base64,{base64_pdf}" width="1100" height="900" type="application/pdf"></iframe>'
#     st.markdown(pdf_display, unsafe_allow_html=True)


# def show_pdf(file_path):
#     with open(file_path, "rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode("utf-8")
#     pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
#     st.markdown(pdf_display, unsafe_allow_html=True)
