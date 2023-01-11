import streamlit as st

from streamlit_extras.switch_page_button import switch_page
from utils import set_page_config, sidebar_image, set_css, author_link, set_pages


def page_info():
    st.markdown(
        "<h1 style='text-align: center; color: #7A3777;'><strong>Explore <em>Mycobacterium tuberculosis</em> complex</strong></h1>",
        unsafe_allow_html=True,
    )
    st.markdown("---")


def buttons():
    bt1, bt2, bt3, mk = st.columns([1, 1, 1, 7])

    with bt1:
        genotype_user_data = st.button("Genotype VCF")
    with bt2:
        phylogeny = st.button("Explore Phylogeny")
    with bt3:
        dataset = st.button("Reference Dataset")

    if genotype_user_data:
        switch_page("genotype lineage")
    if phylogeny:
        switch_page("phylogeny")
    if dataset:
        switch_page("reference dataset")


if __name__ == "__main__":
    set_page_config()
    sidebar_image()
    set_css()
    author_link()
    set_pages()
    page_info()
    buttons()
