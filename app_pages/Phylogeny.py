import base64
import streamlit as st
from utils import set_page_config, sidebar_image, set_css

set_page_config()
sidebar_image()
set_css()

st.title("_Mycobacterium tuberculosis_ phylogeny")

st.markdown("---")


def show_svg(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f'<iframe src="data:image/svg+xml;base64,{base64_pdf}" width="1100" height="900" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    # Embedding PDF in HTML
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></embed>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Lineage 1",
        "Lineage 2",
        "Lineage 3",
        "Lineage 4",
        "MTBC",
    ]
)

with tab1:
    show_pdf("./data/trees/l1_tree.pdf")

with tab2:
    show_svg("./data/trees/lineage2_tree.svg")

with tab3:
    show_svg("./data/trees/lineage3_tree.svg")

with tab4:
    show_svg("./data/trees/lineage4_tree.svg")

with tab5:
    show_svg("./data/trees/mtbc_tree.svg")

# # TREE TEST

# HtmlTree = open("./data/tree-plot.html", "r", encoding="utf-8")
# source_code = HtmlTree.read()
# components.html(source_code, height=1500, scrolling=True)
