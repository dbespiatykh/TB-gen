import streamlit as st  # 🎈 data web app development
import streamlit.components.v1 as components
import base64

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
