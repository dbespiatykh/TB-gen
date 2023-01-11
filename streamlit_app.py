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
    bt1, bt2, bt3, bt4, bt5 = st.columns([4, 1, 1, 1, 4])

    with bt1:
        pass
    with bt2:
        genotype_user_data = st.button("Genotype VCF")
    with bt3:
        phylogeny = st.button("Explore Phylogeny")
    with bt4:
        dataset = st.button("Reference Dataset")
    with bt5:
        pass

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
