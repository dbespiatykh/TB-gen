import streamlit as st
import leafmap.kepler as leafmap

from streamlit_extras.switch_page_button import switch_page
from utils import set_page_config, sidebar_image, set_css
from st_pages import Page, show_pages

set_page_config()
sidebar_image()
set_css()

show_pages(
    [
        Page("streamlit_app.py", "Home", "🏠"),
        Page("app_pages/Reference_dataset.py", "Reference dataset", "📈"),
        Page("app_pages/Phylogeny.py", "Phylogeny", "🧬"),
        Page("app_pages/Genotype_lineage.py", "Genotype lineage", "📊"),
    ]
)

st.sidebar.success("Select a page above")

st.sidebar.header("Header `ver 1`")
st.sidebar.subheader("Subheader")

st.title("Global _Mycobacterium tuberculosis_ data")
st.markdown(
    """
Add description
"""
)


genotype_user_data = st.button("Genotype VCF")

if genotype_user_data:
    switch_page("genotype lineage")
